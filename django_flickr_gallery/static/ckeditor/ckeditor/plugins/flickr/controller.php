<?php
/**
 * Controller for interacting with Flickr
 */
header('Content-type: application/json');
require_once 'Flickr.php';

$apiKey 	= '<Add your API Key here>';
$userId 	= '<Add your user ID here>';
$baseUrl 	= '<Add URL to your profile incl trailing slashe>'; //eg. http://www.flickr.com/photos/simon_jensen/

$flickr 	= new Flickr($apiKey, $userId, $baseUrl);

$perPage 	= isset($_POST['perPage']) ? $_POST['perPage'] : 50;
$page 		= isset($_POST['page']) ? $_POST['page'] : 1;
$photos 	= json_encode($flickr->getPhotos($page, $perPage));

echo $photos;
exit;
?>