<?php
$site = 'http://spacecareers.us/';
$username = "job.import";
$password = "fg8cm4gv#wLoNT^B2*Tn^RLg";
// xml that will change title for job with id=63
$xml = "";

// import setup
$path = 'wp-admin/admin-ajax.php';
$url = $site.$path;
$data = array(
 'username' => $username,
 'password' => $password,
 'xml' => $xml,
 'action' => 'wpjb_import_api'
);

$options = array(
 'http' => array(
 'header' => "Content-type: application/x-www-form-urlencoded",
 'method' => 'POST',
 'content' => http_build_query($data),
 ),
);

$context = stream_context_create($options);
$result = file_get_contents($url, false, $context);
$result = simplexml_load_string($result);

// parsing results
foreach($result->import as $import) {
  $type = (string)$import->type;
  $title = (string)$import->title;
  $action = (string)$import->action;
  echo "$action $type: $title<br/>";
  if(is_array($import->messages->message)) {
    foreach($import->messages->message as $message) {
      echo "- " . (string)$message->text."<br/>";
    }
  }
  echo "<br/>";
}
