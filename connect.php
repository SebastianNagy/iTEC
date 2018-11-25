<?php
$db_host="localhost:3306";
$db_username="itec";
$db_password="cmfsebi";
$db_select="scriecoord";
$conexiune=mysqli_connect($db_host,$db_username,$db_password,$db_select);
if(!mysqli_select_db($conexiune,$db_select))
echo "nu merge select_db\n";
else
echo "merge select_db\n";

?>
