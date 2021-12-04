<?php
    require 'database.php';
    $id_tag = 0;
     
    if ( !empty($_GET['id_tag'])) {
        $id_tag = $_REQUEST['id_tag'];
    }
     
    if ( !empty($_POST)) {
        // keep track post values
        $id = $_POST['id_tag'];
         
        // delete data
        $pdo = Database::connect();
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $sql = "DELETE FROM item_data_matahari  WHERE id_tag = ?";
        $q = $pdo->prepare($sql);
        $q->execute(array($id_tag));
        Database::disconnect();
        header("Location: item_data.php");
         
    }
?>
 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <link   href="css/bootstrap.min.css" rel="stylesheet">
    <script src="js/bootstrap.min.js"></script>
	<title>Delete : MATAHARI ITEM INFORMATION</title>
</head>
 
<body>
	<h2 align="center">MATAHARI ITEM INFORMATION</h2>

    <div class="container">
     
		<div class="span10 offset1">
			<div class="row">
				<h3 align="center">Delete Item</h3>
			</div>

			<form class="form-horizontal" action="item data delete page.php" method="post">
				<input type="hidden" name="id" value="<?php echo $id;?>"/>
				<p class="alert alert-error">Are you sure to delete ?</p>
				<div class="form-actions">
					<button type="submit" class="btn btn-danger">Yes</button>
					<a class="btn" href="item_data.php">No</a>
				</div>
			</form>
		</div>
                 
    </div> <!-- /container -->
  </body>
</html>