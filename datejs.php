<?php

require_once('config.php');
include("connect.php");

//print 'Cerere inserare trimisa\n';
echo "Cerere inserare trimisa\n";
if (isset($_POST["points"])) 
{
    
    $points = json_decode($_POST["points"]);
    // echo "Data is: " . $points->data . "<br>";
   // echo "Point 1: " . $points->data[1] . ", " . $points->arPoints[0]->y;
    $lungime = $points->lungime;
    
    for($j=1;$j<$lungime;$j++){
    	print $points->data[$j].',';
    }
	
	$date = $lungime.';'; 
    for($j=1;$j<$lungime;$j++){
    	//print $points->data[$j].'  ';
        $date =$date.$points->data[$j].',';
    } 


$update = "UPDATE scriecoord SET coord='".$date."'";
//$update="INSERT INTO scriecoord (scriecoord) VALUES ('".$date."')";
if(mysqli_query($conexiune, $update)){
echo ("\nO mers scrierea in baza de date");}
else{
printf ("CSF ma MYSQLF -- %s" ,mysqli_error($conexiune));}
exec('sudo python baza2.py');

}
else 
echo "\nPai ce-ai facut ma nene maaa n-am primit cu $_POST.\n";   

?>
