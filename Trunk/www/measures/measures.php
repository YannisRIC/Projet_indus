<?php

    require_once("../orm/Measure.php");

    $xlast = isset ($_GET["xlast"]) ? $_GET["xlast"] : "undefined";
    $time  = isset ($_GET["time"]) ? $_GET["time"] : "undefined";

    $id  = explode('/', $_SERVER['PATH_INFO'])[1];

    $tableObject = new Measure();

    //If both of parameter are not given get all measures
    if($xlast == "undefined" and $time == "undefined"){
        //If id in url select device selected
        if($id != ""){
            $cond = array("hardwareConfigurationId" => array("=", $id));
            $res = $tableObject->getRows($cond);
        }
        else{
            $res = $tableObject->getAll();
        }
    }
    //If both parameter are given get data
    else if($xlast != "undefined" and $time != "undefined"){
        $cond = array("timestamp" => array(">=", $time));
        if($id != ""){
            $cond += array("hardwareConfigurationId" => array("=", $id));
        }
	   $res = $tableObject->getRowsLimited($cond, $xlast);
    }
    //If xlast alone
    else if($xlast != "undefined" and $time == "undefined"){
        if($id != ""){
            $cond = array("hardwareConfigurationId" => array("=", $id));
            $res = $tableObject->getRowsLimited($cond, $xlast);
        }
	   $res = $tableObject->getAllLimited($xlast);
    }
    //If time alone
    else if($xlast == "undefined" and $time != "undefined"){
        $cond = array("timestamp" => array(">=",$time));
        if($id != ""){
            $cond += array("hardwareConfigurationId" => array("=", $id));
        }
	$res = $tableObject->getRows($cond);
    }
    
    $i= 0;
    $o["measures"] = "";

	foreach ($res as $value) {
		$o["measures"][$i] = $value;
		$i++;
	}

    if(empty($o["measures"])){
        $o="";
        $o["code"]=404;
        $o["message"]= "Not found";
    }

	header('Content-Type: application/json');
	echo json_encode($o);
?>