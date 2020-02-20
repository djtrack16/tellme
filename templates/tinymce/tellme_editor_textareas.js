tinyMCE.init({
    mode : "textareas",
    theme : "advanced",
    skin : "tellme",
    plugins: "save,paste",
    theme_advanced_buttons1 : "save,cancel,|,bold,italic,underline,strikethrough,|,cut,copy,paste,pastetext,|,forecolor,backcolor,|,justifyleft,justifycenter,justifyright,justifyfull,|,fontselect,fontsizeselect,",
    theme_advanced_buttons2 : "",
    theme_advanced_buttons3 : "",
    theme_advanced_disable : "cancel,",
    theme_advanced_toolbar_location : "top",
    theme_advanced_toolbar_align : "left",
    theme_advanced_resizing : true,
    width : "100%",
    height : "100%"
    ,save_enablewhendirty : true
    ,save_onsavecallback : mceAjaxSave
    ,init_instance_callback : init_tb
    ,setup : function(ed) {
        ed.onKeyPress.add(function(ed, e) {
            ed.isNotDirty = 0;
            ed.nodeChanged();
        });
     }
});

function mceAjaxSave() {
        var ed = tinyMCE.activeEditor;

        // Do you ajax call here, window.setTimeout fakes ajax call
        ed.setProgressState(1); // Show progress
        $.ajax({
            url: window.location,
            type: 'POST',
            data: {'body': ed.getContent()},
            complete: function() {
                ed.setProgressState(0);
                ed.isNotDirty = 1;
                ed.nodeChanged();
            }
        });
}
