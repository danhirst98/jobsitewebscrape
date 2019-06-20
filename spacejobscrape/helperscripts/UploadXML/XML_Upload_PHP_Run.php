<?php
$site = 'http://spacecareers.us/';
$username = "job.import";
$password = "fg8cm4gv#wLoNT^B2*Tn^RLg";
// xml that will change title for job with id=63
$xml = "<wpjb>
  <jobs>
    <job>
      <id>2504357445</id>
    <job_expires_at>2019-05-31</job_expires_at>
    <is_active>1</is_active>
    <is_approved>1</is_approved>
    </job>
  <job>
      <id>3790762986</id>
    <job_expires_at>2019-05-31</job_expires_at>
    <is_active>1</is_active>
    <is_approved>1</is_approved>
    </job>
  <job>
      <id>187043526</id>
    <job_expires_at>2019-05-31</job_expires_at>
    <is_active>1</is_active>
    <is_approved>1</is_approved>
    </job>
  <job>
      <id>3520402574</id>
    <job_expires_at>2019-05-31</job_expires_at>
    <is_active>1</is_active>
    <is_approved>1</is_approved>
    </job>
  <job>
      <id>594163367</id>
    <job_expires_at>2019-05-31</job_expires_at>
    <is_active>1</is_active>
    <is_approved>1</is_approved>
    </job>
  <job>
      <id>1838366571</id>
    <job_expires_at>2019-05-31</job_expires_at>
    <is_active>1</is_active>
    <is_approved>1</is_approved>
    </job>
  </jobs>
</wpjb>
";

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
