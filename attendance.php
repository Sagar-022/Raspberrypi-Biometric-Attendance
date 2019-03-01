<?php $dbc = @mysqli_connect('localhost', 'hannan', 'tech', 
'attendance') OR die('Could not connect to MySQL: ' .
    mysqli_connect_error()); ?> <html>
	<head>
		<title>Attendance Sheet</title>
	</head>
	<body>
		<style>
			table {
				border-collapse: collapse;
				border: 1px solid black;
				margin: 10px;
			}
			td, th {
				border: 1px solid black;
				padding: 5px;
			}
			td.present {
				color: black;
				background-color: lime;
			}
			td.absent {
					color: white;
					background-color: red;
			}
		</style>
		<table>
			<?php
			$response = $dbc->query("select cc from 
current_class_no;");
			$row = $response->fetch_array();
			$classCount = $row['cc'];
			?>
			
			<tr><th>Roll</th><th>Name</th><?php for 
($i=1;$i<=$classCount;$i++)echo "<th>".$i."</th>";?></tr>
			
			<?php
			$response = $dbc->query("select roll, name from 
student;");
			while ($row = $response->fetch_array()) {
				$roll = $row['roll'];
				$name = $row['name'];
				?>
				<tr>
					<td><?php echo 
$roll;?></td><td><?php echo $name;?></td>
				<?php
				$response2 = $dbc->query("select attend 
from sheet where roll = '".$roll."' order by class_no;");
				while ($row2 = 
$response2->fetch_array()) {
					if ($row2['attend']=="Present")
						echo "<td 
class=\"present\">P</td>";
					else
						echo "<td 
class=\"absent\">X</td>";
				}
			}
			?>
		</table>
	</body> </html>
