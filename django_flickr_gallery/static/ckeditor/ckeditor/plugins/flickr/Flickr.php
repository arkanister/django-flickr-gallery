<?php
/**
 * Simple class for fetching photos to some Flick user
 * @author	Simon Jensen
 */
class Flickr {
	
	/**
	 * @var		string
	 */
	private $apiKey		= '';
	
	/**
	 * @var		string
	 */
	private $userId		= '';
	
	/**
	 * @var		string
	 */
	private $baseUrl	= '';
	

	/**
	 * @var 	integer
	 */
	private $perPage 	= 10;
	

	/**
	 * @var 	integer
	 */
	private $page 		= 1;


	/**
	 * @var 	integer
	 */
	private $numOfPages = 0;


	/**
	 * @author	Simon Jensen
	 * @param 	string 			$apiKey
	 * @param 	string 			$userId
	 * @param 	string 			$baseUrl
	 * @return 	void
	 */
	public function __construct($apiKey, $userId, $baseUrl)
	{
		$this->apiKey 	= $apiKey;
		$this->userId 	= $userId;
		$this->baseUrl 	= $baseUrl;
	}


	/**
	 * @author	Simon Jensen
	 * @param	string			$userId
	 * @param	integer			$page
	 * @param	integer			$perPage
	 * @return	array
	 */
	public function getPhotos($page = 1, $perPage = 10)
	{
		$params		= array(
			'api_key'	=> $this->apiKey,
			'method'	=> 'flickr.people.getPublicPhotos',
			'format'	=> 'php_serial',
			'per_page'	=> $perPage,
			'page'		=> $page,
			'user_id'	=> $this->userId
		);
		
		$encoded_params	= array();
		foreach ($params as $key => $value) {
			$encoded_params[]	= urlencode($key) . '=' . urlencode($value);
		}
		
		$curl			= curl_init();
		curl_setopt($curl, CURLOPT_URL, 'http://api.flickr.com/services/rest/');
		curl_setopt($curl, CURLOPT_POST, 1);
		curl_setopt($curl, CURLOPT_POSTFIELDS, implode('&', $encoded_params));
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($curl, CURLOPT_CONNECTTIMEOUT, 10);
		
		$result			= curl_exec($curl);
		
		// Check result
		if (!$result) {
			return array();
		}
		
		$result			= unserialize($result);
		if ($result['stat'] != "ok") {
			return array();
		}
		
		// Store number of pages info
		$this->perPage 		= $perPage;
		$this->page 		= $page;
		$this->numOfPages 	= $result['photos']['pages'];
		$this->numOfPhotos 	= $result['photos']['total'];
		
		// Array to be returned
		$photos			= array();
		foreach ($result['photos']['photo'] as $photo) {
			$object						= new stdClass();
			$object->title				= $photo['title'];
			$object->flickr				= $this->getFlickrUrl($photo);
			$object->flickrLightbox		= $this->getFlickrUrl($photo, true);
			$object->image				= $this->getPhotoUrl($photo);
			$photos[]					= $object;
		}

		// Add pagenation info to last position in array
		$object						= new stdClass();
		$object->perPage 			= $this->perPage;
		$object->page 				= $this->page;
		$object->numOfPages 		= $this->numOfPages;
		$object->numOfPhotos 		= $this->numOfPhotos;
		$photos[] 					= $object;
		
		return $photos;
	}
	
	
	/**
	 * Get URL on Flickr for a Photo
	 * @param	array			$photo
	 * @param	boolean			$lightBox
	 * @return	string
	 */
	private function getFlickrUrl($photo = array(), $lightbox = false)
	{
		if ($lightbox) {
			return $this->baseUrl.$photo['id'].'/lightbox/';
		}
		return $this->baseUrl.$photo['id'].'/';
	}
	
	
	/**
	 * Get URL for a Photo
	 * Possible size options are:
	 * s	small square 75x75
	 * q	large square 150x150
	 * t	thumbnail, 100 on longest side
	 * m	small, 240 on longest side
	 * n	small, 320 on longest side
	 * -	medium, 500 on longest side
	 * z	medium 640, 640 on longest side
	 * c	medium 800, 800 on longest side†
	 * b	large, 1024 on longest side
	 * o	original image, either a jpg, gif or png, depending on source format
	 * @param	array			$photo
	 * @param	string			$size
	 * @return	string
	 */
	private function getPhotoUrl($photo = array(), $size = 's')
	{
		return 'http://farm'.$photo['farm'].'.static.flickr.com/'.$photo['server'].'/'.$photo['id'].'_'.$photo['secret'].'_'.$size.'.jpg';
	}
	
}
?>