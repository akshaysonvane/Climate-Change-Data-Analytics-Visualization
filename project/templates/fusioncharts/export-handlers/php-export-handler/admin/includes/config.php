<?php

date_default_timezone_set('Asia/Kolkata');
$host = "ec2-54-183-213-41.us-west-1.compute.amazonaws.com" ;
$user = "root";
$pass = "root";
$db = "exportserverdb";
$con = mysql_connect($host,$user,$pass);
if (!$con)
{
  die('Could not connect: ' . mysql_error());
}
$db_selected = mysql_select_db($db, $con);
if (!$db_selected) {
    die ('Can\'t use '. $db . mysql_error());
}
