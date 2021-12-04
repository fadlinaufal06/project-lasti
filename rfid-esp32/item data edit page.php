<?php
    require 'database.php';
    $id_tag = null;
    if ( !empty($_GET['id_tag'])) {
        $id_tag = $_REQUEST['id_tag'];
    }
     
    $pdo = Database::connect();
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	$sql = "SELECT * FROM item_data_matahari where id_tag = ?";
	$q = $pdo->prepare($sql);
	$q->execute(array($id_tag));
	$data = $q->fetch(PDO::FETCH_ASSOC);
	Database::disconnect();
?>

<!DOCTYPE html>
<html lang="en">
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta charset="utf-8">
		<link href="css/bootstrap.min.css" rel="stylesheet">
		<script src="js/bootstrap.min.js"></script>
		
		<style>
		html {
			font-family: Arial;
			display: inline-block;
			margin: 0px auto;
		}
		
		textarea {
			resize: none;
		}

		ul.topnav {
			list-style-type: none;
			margin: auto;
			padding: 0;
			overflow: hidden;
			background-color: #4CAF50;
			width: 70%;
		}

		ul.topnav li {float: left;}

		ul.topnav li a {
			display: block;
			color: white;
			text-align: center;
			padding: 14px 16px;
			text-decoration: none;
		}

		ul.topnav li a:hover:not(.active) {background-color: #3e8e41;}

		ul.topnav li a.active {background-color: #333;}

		ul.topnav li.right {float: right;}

		@media screen and (max-width: 600px) {
			ul.topnav li.right, 
			ul.topnav li {float: none;}
		}
		</style>
		
		<title>Edit : MATAHARI ITEM INFORMATION</title>
		
	</head>
	
	<body>

		<h2 align="center">MATAHARI ITEM INFORMATION</h2>
		
		<div class="container">
     
			<div class="center" style="margin: 0 auto; width:495px; border-style: solid; border-color: #f2f2f2;">
				<div class="row">
					<h3 align="center">Edit Item Data</h3>
					<!-- <p id="defaultGender" hidden><?php echo $data['harga'];?></p> -->
				</div>
		 
				<form class="form-horizontal" action="item data edit tb.php?id=<?php echo $id_tag?>" method="post">
					<div class="control-group">
						<label class="control-label">ID</label>
						<div class="controls">
							<input name="id_tag" type="text"  placeholder="" value="<?php echo $data['id_tag'];?>" readonly>
						</div>
					</div>
					
					<div class="control-group">
						<label class="control-label">Nama</label>
						<div class="controls">
							<input name="nama" type="text"  placeholder="" value="<?php echo $data['nama'];?>" required>
						</div>
					</div>
					
					<div class="control-group">
						<label class="control-label">Keterangan</label>
						<div class="controls">
							<!-- <select name="gender" id="mySelect">
								<option value="Male">Male</option>
								<option value="Female">Female</option>
							</select> -->
							<input name="add_info" type="text"  placeholder="" value="<?php echo $data['add_info'];?>" required>
						</div>
					</div>
					
					<div class="control-group">
						<label class="control-label">Harga</label>
						<div class="controls">
							<input name="harga" type="text" placeholder="" value="<?php echo $data['harga'];?>" required>
						</div>
					</div>
					
					<div class="control-group">
						<label class="control-label">Stok</label>
						<div class="controls">
							<input name="stok" type="text"  placeholder="" value="<?php echo $data['stok'];?>" required>
						</div>
					</div>
					
					<div class="form-actions">
						<button type="submit" class="btn btn-success">Update</button>
						<a class="btn" href="item_data.php">Back</a>
					</div>
				</form>
			</div>               
		</div> <!-- /container -->	
		
		<!-- <script>
			var g = document.getElementById("defaultGender").innerHTML;
			if(g=="Male") {
				document.getElementById("mySelect").selectedIndex = "0";
			} else {
				document.getElementById("mySelect").selectedIndex = "1";
			}
		</script> -->
	</body>
</html>