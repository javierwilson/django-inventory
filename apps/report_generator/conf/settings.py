#TINYMCE_JS_URL (default: settings.MEDIA_URL + 'js/tiny_mce/tiny_mce.js')
#The URL of the TinyMCE javascript file.
#TINYMCE_JS_ROOT (default: settings.MEDIA_ROOT + 'js/tiny_mce')
#The filesystem location of the TinyMCE files.
#TINYMCE_DEFAULT_CONFIG (default: {'theme': "simple", 'relative_urls': False})
#The default TinyMCE configuration to use. See the TinyMCE manual for all options. To set the configuration for a specific TinyMCE editor, see the mce_attrs parameter for the widget.
#TINYMCE_SPELLCHECKER (default: False)
#Whether to use the spell checker through the supplied view. You must add spellchecker to the TinyMCE plugin list yourself, it is not added automatically.
#TINYMCE_COMPRESSOR (default: False)
#Whether to use the TinyMCE compressor, which gzips all Javascript files into a single stream. This makes the overall download size 75% smaller and also reduces the number of requests. The overall initialization time for TinyMCE will be reduced dramatically if you use this option.
#TINYMCE_FILEBROWSER (default: True if 'filebrowser' is in INSTALLED_APPS, else False)
#Whether to use django-filebrowser as a custom filebrowser for media inclusion. See the official TinyMCE documentation on custom filebrowsers.

TINYMCE_DEFAULT_CONFIG = {
    #'plugins' : "safari,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,imagemanager,filemanager",
    'plugins': "table,spellchecker,paste,searchreplace,style",
    'theme': "advanced",
    'theme_advanced_buttons1' : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
    'theme_advanced_buttons2' : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
    'theme_advanced_buttons3' : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
    'theme_advanced_buttons4' : "insertlayer,moveforward,movebackward,absolute,|,styleprops,spellchecker,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,nonbreaking,template,blockquote,pagebreak,|,insertfile,insertimage,|,special",
#       'setup' : "function(ed) {\
#                       // Add Custom Code\
#                       ed.addButton('special', {\
#                                       title : 'This is an example description',\
#                                       image : 'images/example.gif',\
#                                       onclick : function() {\
#                                                       alert( ed.selection.getContent({format : 'text'}) );\
#                                       }\
#                       });\
#       }",
        #'extended_valid_elements' : "pdf:pagenumber[]",
        #'valid_elements' : "pdf:pagenumber",
        #'extended_valid_elements' : "pdf:pagenumber",
        #'custom_elements' : "pdf:pagenumber",
        'theme_advanced_toolbar_location' : "top",
        'theme_advanced_toolbar_align' : "left",
        'theme_advanced_statusbar_location' : "bottom",
        'theme_advanced_resizing' : True
        #'entity_encoding': "numeric",
        #'entities' : "160,nbsp,38,amp,34,quot,162,cent,8364,euro,163,pound,165,yen,169,copy,174,reg,8482,trade,8240,permil,60,lt,62,gt,8804,le,8805,ge,176,deg,8722,minus"
        #'entities' : "160,nbsp,38,&,60,<,62,>,8722,-"
}
