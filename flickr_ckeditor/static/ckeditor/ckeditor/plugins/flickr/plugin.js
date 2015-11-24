CKEDITOR.plugins.add('flickr',
{
	requires : [ 'dialog' ],
	init: function(editor)
	{
		var command 		= editor.addCommand( 'flickr', new CKEDITOR.dialogCommand( 'flickr' ) );
		command.modes 		= { wysiwyg:1, source:0 };
		command.canUndo 	= false;
		command.readOnly 	= 1;
		
		editor.ui.addButton('Flickr',
		{
			label: 'Flickr',
			command: 'flickr',
			icon: this.path + 'flickr.png'
		});

		CKEDITOR.dialog.add( 'flickr', this.path + 'dialogs/flickr.js' );
	}
});