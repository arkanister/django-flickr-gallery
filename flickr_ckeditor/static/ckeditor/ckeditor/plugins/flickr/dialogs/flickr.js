var $ = django.jQuery;

CKEDITOR.dialog.add('flickr', function(editor)
{
	return {
		title: 'Flickr',
		minWidth: 820,
		minHeight: 500,
		contents: [
			{
				id: 'photos',
				label: 'Photos',
				elements:
				[
                    {
						type: 'html',
						html:
                            '<div id="flickr-photoset">' +
                            '<label class="cke_dialog_ui_labeled_label" for="flickr-photoset-select" style="padding-bottom: 10px; display: block;">Select photoset</label>' +
                            '<div class="cke_dialog_ui_labeled_content">' +
                            '<div class="cke_dialog_ui_input_select"><select class="cke_dialog_ui_input_select" id="flickr-photoset-select"></select></div>' +
                            '</div></div>'
					},
                    {
						type: 'html',
						html:
                        '<style type="text/css">' +
                        '.label.label-flickr { background-color: #F20072; color: #fff; padding: 2px 4px; }' +
                        '</style>' +
                        '<div id="flickr-resume"></div>'
					},
                    {
                        type: 'html',
                        html:
                        '<style type="text/css">' +
                        '#flickr-paging { float: right; margin-top: -30px; margin-right: 5px; }' +
                        '#flickr-paging a.paging { font-weight: bold; padding: 2px 5px; margin: 0 2px; color: #fff; background: rgb(60,118,229); }' +
                        '#flickr-paging a.current, #flickr-paging a.paging:hover { background: rgb(242,0,114); }' +
                        '#flickr-photos { width: 840px; position: relative; max-height: 500px; overflow-y: auto; }' +
                        '#flickr-photos a { display: block; float: left; }' +
                        '#flickr-photos img { border: 5px solid white; margin: 2px; }' +
                        '#flickr-photos img.selected, #flickr-photos img:hover { border-color: rgb(242,0,114); }' +
                        '</style>' +
                        '<div id="flickr-paging">Page: </div>' +
                        '<div id="flickr-photos"></div>'
                    }
                ]
			}
		],
		onOk : function() {
			var dialog			= this,
				data			= {},
				link			= editor.document.createElement('a'),
				selectedPhoto 	= $('img.selected');

			selectedPhoto.removeAttr('class');

			this.commitContent(data);

			link.setAttribute('href', selectedPhoto.attr('rel'));

			link.setAttribute('target', '_blank' );

			link.setAttribute('title', selectedPhoto.attr('alt'));

			link.setHtml('<img src="' + selectedPhoto.attr('data-url') + '" alt="' + selectedPhoto.attr('alt') + '" />');

			editor.insertElement(link);
		},
        onShow: function() {
            flickrLoadPage(20, 1, null);
        }
	};
});

function flickrSelectPhoto(id) {
	$('.selected').removeClass('selected');
	$('#'+id).addClass('selected');
}

function flickrLoadPage(perPage, page, photoset) {

    $('#flickr-photos').html('<em>Loading ...</em>');

	$.get('/ckeditor/flickr/', {'per-page': perPage, page: page, photoset: photoset }, function(data) {

		// Reset
		$("#flickr-paging").html('Page: ');
		$("#flickr-photos").html('');
		$("#flickr-resume").html('');
        $("#flickr-photoset-select").html('<option value="">----------</option>');

		// Render pagenation
		var numOfPages	= data.numOfPages;
		var totalOfPhotos	= data.totalOfPhotos;
        var photosets   = data.photosets;
		var pages 		= '';
		var options 	= '';

		for (var i = 1; i <= numOfPages; i++) {
			pages += '<a class="paging ' + (i == page ? 'current' : '') + '" href="#" data-page="' + i + '" data-paging="flickr">' + i + '</a>';
		};

        for (var i = 0; i < photosets.length; i++) {
            options += '<option value="' + photosets[i][0] + '"' + (photoset == photosets[i][0] ? 'selected="selected"' : '') + '>' + photosets[i][1] + '</option>';
        }

		$("#flickr-paging").append(pages);
        $("#flickr-photoset-select").append(options);
        $("#flickr-resume").append('<span class="label label-flickr label-default">' + (totalOfPhotos ? totalOfPhotos : 0) +' PHOTOS</span>');

        $("#flickr-photoset-select").unbind().on('change', function () {
            flickrLoadPage(perPage, 1, $(this).val());
        });

        $("[data-paging='flickr']").unbind().on('click', function () {
            //  data-per-page="' + perPage + '" data-page="' + page + '" data-photoset-id="' + photoset + '"
            flickrLoadPage(perPage, $(this).attr('data-page'), photoset);
        });

        if ('errors' in data) {
            $("#flickr-resume").html('');
            $('#flickr-photos').html('');

            for (var i = 0; i < data.errors.length; i++) {
                $('#flickr-photos').append('<p style="color: red;">' + data.errors[i] + '</p>');
            }

            return false;
        }

        // if not photos
        if (data.photos.length == 0) {
            $("#flickr-resume").html('');

            if (photoset == null || photoset == '' || photoset == undefined) {
                $('#flickr-photos').html('<em>Select a photoset</em>');
            } else {
                $('#flickr-photos').html('<em>No photos to photoset</em>');
            }

            return false;
        }

		// Render photos
		var image		= '';
		$.each(data.photos, function(index, value) {

			image =  '<a href="javascript:flickrSelectPhoto(\'flickr_' + index + '\');">';
			image += '<img class="flickrPhoto" id="flickr_' + index + '" rel="' + value.absolute_lightbox_url + '" data-url="' + value.url_m + '" " src="' + value.url_q + '" alt="' + value.title + '" />';
            image += '</a>';

			$("#flickr-photos").append(image);
		});

	},'json');
}