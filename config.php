<?php
session_start();
set_time_limit(0);
error_reporting(E_ALL);

// Informatii baza de date

 $AdresaBazaDate = "localhost:3306";
 $UtilizatorBazaDate = "itec";
 $ParolaBazaDate = "cmfsebi";
 $NumeBazaDate = "scriecoord";

 $conexiune = mysqli_connect($AdresaBazaDate,$UtilizatorBazaDate,$ParolaBazaDate,$NumeBazaDate);
 if(!$conexiune){
 die("Nu ma pot conecta la MySQL!  SAAAU nu gaseste baza de date" );
}
else {echo "\nM-am conectat la baza de date \n";}
 mysqli_select_db($conexiune,$NumeBazaDate) or die("Nu gasesc baza de date\n" . mysql_error());

// End addentities() --------------

/*print '<script language="JavaScript" type="text/JavaScript">

function MM_openBrWindow(theURL,winName,features) {
window.open(theURL,winName,features);


}
</script>';
*/


?>
