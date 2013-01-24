function expand_related(event, model, field, path, path_verbose) {
    if (event.target.tagName != 'LI') return;
    var element = $(event.target);
    if ( $(element).hasClass('tree_closed') ){
        $.get(
              // Fix the URL for our app. FIXME: Make this less brittle!!
            "/reports/ajax_get_related/",
            {model: model, field: field, path: path, path_verbose: path_verbose},
            function(data){
                $(element).addClass('tree_expanded');
                $(element).removeClass('tree_closed');
                $(element).after('<li>' + data + '</li>');
            }
        );
    } else{
        $(element).addClass('tree_closed');
        $(element).removeClass('tree_expanded');
        $(element).next().remove();
    }
}

function show_fields(event, model, field, path, path_verbose){
    $('.highlight').removeClass('highlight');
    $(event.target).addClass('highlight');
    $.get(
        "/reports/ajax_get_fields/",
        {model: model, field: field, path: path, path_verbose: path_verbose},
        function(data){
            $('#field_selection_div').html(data);

            enable_drag();
        }
    );
}

function addFieldList(el) {
  field = $.trim($(el).text());
  name = $.trim($(el).data('name'));
  path_verbose = $.trim($(el).data('path_verbose'));
  path = $.trim($(el).data('path'));

  if (name == '') return;

  // Check for duplicates
  if ($("table#field_list_table input[type='hidden'][name$='field'][value='" + name + "']").length > 0) return;

  total_forms = $('#id_displayfield_set-TOTAL_FORMS');
  i = total_forms.val();
  total_forms.val(parseInt(i)+1);

  var row_html = '<tr><td><span style="cursor: move;" class="ui-icon ui-icon-arrowthick-2-n-s"></span></td>';
  row_html += '<td><input id="id_displayfield_set-'+i+'-field_verbose" name="displayfield_set-'+i+'-field_verbose" readonly="readonly" type="text" value="' + field + '"/><input id="id_displayfield_set-'+i+'-path" name="displayfield_set-'+i+'-path" type="hidden" value="' + path + '"/></td>';
  row_html += '<td><input id="id_displayfield_set-'+i+'-field" name="displayfield_set-'+i+'-field" type="hidden" value="' + name + '"/>'
  row_html += '<input id="id_displayfield_set-'+i+'-name" name="displayfield_set-'+i+'-name" type="text" value="' + name + '"/></td>';
  row_html += '<input type="checkbox" name="displayfield_set-'+i+'-sort_reverse" id="id_displayfield_set-'+i+'-sort_reverse"></td>';
  row_html += '<td><input type="checkbox" name="displayfield_set-'+i+'-DELETE" id="id_displayfield_set-'+i+'-DELETE">';
  row_html += '<span class="hide_me"><input type="text" name="displayfield_set-'+i+'-position" value="999" id="id_displayfield_set-'+i+'-position"></span></td>';
  row_html += '</tr>';
  $('#field_list_table > tbody:last').append(row_html);
}

function addFieldFilter(el) {
  field = $.trim($(el).text());
  name = $.trim($(el).data('name'));
  path_verbose = $.trim($(el).data('path_verbose'));
  path = $.trim($(el).data('path'));

  if (name == '') return;

  // Check for duplicates
  if ($("table#field_filter_table input[type='hidden'][name$='field'][value='" + name + "']").length > 0) return;

  total_forms = $('#id_fil-TOTAL_FORMS');
  i = total_forms.val();
  total_forms.val(parseInt(i)+1);

  row_html = '<tr>'
  row_html += '<td><span style="cursor: move;" class="ui-icon ui-icon-arrowthick-2-n-s"></span></td>'
  row_html += '<td><input type="hidden" name="fil-'+i+'-field" value="'+ name +'" id="id_fil-'+i+'-field">'
  row_html += '<input name="fil-'+i+'-field_verbose" value="'+ field +'" readonly="readonly" maxlength="2000" type="text" id="id_fil-'+i+'-field_verbose">'
  row_html += '<input type="hidden" value="'+ path +'" name="fil-'+i+'-path" id="id_fil-'+i+'-path"></td>'
  row_html += '<td><select onchange="check_filter_type(event.target)" name="fil-'+i+'-filter_type" id="id_fil-'+i+'-filter_type">'
  row_html += '<option value="">---------</option>\
  <option value="iexact">Equals</option>\
  <option value="icontains" selected="selected">Contains</option>\
  <option value="gt">Greater than</option>\
  <option value="lt">Less than</option>\
  <option value="range">range</option>\
  </select></td>'
  if ( field.indexOf("DateField") > 0 ) {
    row_html += '<td><input class="datepicker" id="id_fil-'+i+'-filter_value" type="text" name="fil-'+i+'-filter_value" value="" maxlength="2000"></td>'
  } else {
    row_html += '<td><input id="id_fil-'+i+'-filter_value" type="text" name="fil-'+i+'-filter_value" value="" maxlength="2000"></td>'
  }
  row_html += '<td><input type="checkbox" name="fil-'+i+'-exclude" id="id_fil-'+i+'-exclude"></td>'
  row_html += '<td><input type="checkbox" name="fil-'+i+'-DELETE" id="id_fil-'+i+'-DELETE">'
  row_html += '<span class="hide_me"><input type="text" name="fil-'+i+'-position" value="0" id="id_fil-'+i+'-position"></span></td>'
  row_html += '</tr>'
  $('#field_filter_table > tbody:last').append(row_html);
  $( ".datepicker" ).datepicker();
}

function enable_drag() {
    $( ".draggable" ).draggable({
        connectToSortable: "#sortable",
        helper: "clone",
        revert: "invalid",
        zIndex: 10000
    });
    $( "#field_list_droppable" ).droppable({
        drop: function(event, ui) {
          addFieldList(ui.draggable.find(".field-button"));
        }
    });
    $( "#field_filter_droppable" ).droppable({
        drop: function( event, ui ) {
          addFieldFilter(ui.draggable.find(".field-button"));
        }
    });
}

function check_filter_type(element){
    var element = $(element);
    selected_type = element.find(":selected").val();
    element.closest('tr').find('input[name=check_value]').remove();
    filter_value = element.closest('tr').find('input[id$=filter_value]');
    switch (selected_type) {
        case 'isnull':
            if ( filter_value.val() && filter_value.val() != '0'  ) {
                filter_value.after('<input name="check_value" onchange="set_check_value(event)" checked="checked" type="checkbox"/>');
            } else {
                filter_value.after('<input name="check_value" onchange="set_check_value(event)" type="checkbox"/>');
                if ( filter_value.val() == "" ) {
                    filter_value.val('0');
                }
            }
            filter_value.hide();
            break;
        default:
            filter_value.show();
    }
}

function set_check_value(event) {
    var element = $(event.target);
    var filter_value = element.closest('tr').find('input[id$=filter_value]');
    if(element.is(':checked')) {
        filter_value.val('1');
    } else {
        filter_value.val('0');
    }
}

function refresh_preview() {
    $.post(
        "/reports/ajax_preview/",
        {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            report_id: $('#report_id').data('id'),
        },
        function(data){
            $('#preview_area').html(data);
        }
    );
}

function aggregate_tip() {
    $('#tip_area').html('Aggregates can have unexpected behavior if used with sort order and the values in your search. To read more check out <a target="_blank" href="https://docs.djangoproject.com/en/dev/topics/db/aggregation/">Django Aggregation</a>')
    $('#tip_area').show('slow');
}

$(function() {
    enable_drag();
    $( "#tabs" ).tabs();
    $("#ui-id-3").click(refresh_preview);

    $('#field_list_table').sortable({
        containment: 'parent',
        zindex: 10,
        items: 'tbody tr',
        handle: 'td:first',
        update: function() {
            $(this).find('tbody tr').each(function(i) {
                if ($(this).find('input[id$=name]').val()) {
                    $(this).find('input[id$=position]').val(i+1);
                }
            });
        }
    });
    $('#field_filter_table').sortable({
        containment: 'parent',
        zindex: 10,
        items: 'tbody tr',
        handle: 'td:first',
        update: function() {
            $(this).find('tbody tr').each(function(i) {
                $(this).find('input[id$=position]').val(i+1);
            });
        }
    });
    $( "#sortable" ).disableSelection();
    // Adjust widgets depending on selected filter type
    $('input[id$=filter_value]').each(function(index, value) {
        element = $(value).closest('tr').find('select[id$=filter_type]');
        check_filter_type(element);
    });
    $( ".datepicker" ).datepicker();
    $('input').change(function() {
        if( $(this).val() != "" )
            window.onbeforeunload = "Are you sure you want to leave?";
    });
    window.onbeforeunload = "Are you sure you want to leave?";

    $(".field-button").dblclick(function(e) {
      var activeTab = $("#tabs li.ui-state-active")
      var tabIndex = $("#tabs li").index(activeTab);
      console.log(tabIndex);
      if (tabIndex == 0) {
        addFieldList(e.target);
      } else if (tabIndex == 1) {
        addFieldFilter(e.target);
      }
    })
});
