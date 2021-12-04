<?php
     
    require 'database.php';
 
    if ( !empty($_POST)) {
        // keep track post values
        $id_tag = $_POST['id_tag'];
		$nama = $_POST['nama'];
		$add_info = $_POST['add_info'];
        $harga = $_POST['harga'];
        $stok = $_POST['stok'];
        
		// insert data
        $pdo = Database::connect();
		$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		$sql = "INSERT INTO item_data_matahari (id_tag,nama,add_info,harga,stok) values(?, ?, ?, ?, ?)";
		$q = $pdo->prepare($sql);
		$q->execute(array($id_tag,$nama,$add_info,$harga,$stok));
		Database::disconnect();
		header("Location: item_data.php");
    }
?>