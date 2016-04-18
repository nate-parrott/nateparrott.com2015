
var stats;

var camera, controls, scene, renderer, raycaster;

init();
animate();

function useAccel() {
	var nav = navigator.userAgent;
	var mobile = false;
	['Android', 'Mobile'].forEach(function(word) {
		if (nav.indexOf(word) != -1) {
			mobile = true;
		}
	})
	return mobile;
}

function init() {

	scene = new THREE.Scene();
	scene.fog = new THREE.FogExp2( 0xcccccc, 0.002 );

	renderer = new THREE.WebGLRenderer();
	renderer.setClearColor( scene.fog.color );
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	
	var pointLight = new THREE.PointLight( 0xffffff, 1.5 );
					pointLight.position.set( 0, 7, 0 );
	scene.add( pointLight );

	document.getElementById('container').appendChild( renderer.domElement );

	camera = new THREE.PerspectiveCamera( 60, window.innerWidth / window.innerHeight, 1, 2000 );
	camera.position.z = 0.5;
	// 						controls = new THREE.DeviceOrientationControls( camera );
	
	if (useAccel()) {
		controls = new THREE.DeviceOrientationControls(camera);
	} else {
		controls = new THREE.OrbitControls( camera, renderer.domElement );
		controls.enableDamping = true;
		controls.dampingFactor = 0.25;
	}
	//controls.addEventListener( 'change', render ); // add this only if there is no animation loop (requestAnimationFrame)
	// controls.enableZoom = false;
	controls.enablePan = false;

	raycaster = new THREE.Raycaster();

	// world
	
	createSkybox();
	// createContent();
	// addGalleryImage('viet.jpg', 180);
	createText();
	
	window.addEventListener( 'resize', onWindowResize, false );

}

function onWindowResize() {

	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	renderer.setSize( window.innerWidth, window.innerHeight );

}

var frame = 0;
function animate() {
	frame++;
	requestAnimationFrame( animate );

	controls.update(); // required if controls.enableDamping = true, or if controls.autoRotate = true
	
	camera.updateMatrixWorld();
	raycaster.setFromCamera( new THREE.Vector2(0,0), camera );
	var intersects = raycaster.intersectObjects( scene.children ).map(function(p){return p.object}).filter(function(obj) {return !!obj.selectable});
	var obj = intersects.length ? intersects[0] : null;
	setSelectedObject(obj);
	
	render();

}

var _selectedObject = null;
var _selectionBackground = null;
function setSelectedObject(obj){
	if (obj !== _selectedObject) {
		if (_selectionBackground) scene.remove(_selectionBackground)
		_selectedObject = obj;
		if (_selectedObject) {
			_selectionBackground = createSelectionBackgroundFromObject(obj);
			scene.add(_selectionBackground)
		}
	}
}

function createSelectionBackgroundFromObject(obj) {
 	var geometry = new THREE.PlaneGeometry( 2, 2);
 	var material = new THREE.MeshBasicMaterial( {color: 0xffffff, side: THREE.DoubleSide} );
	var mesh = new THREE.Mesh(geometry, material);
	// var pos = THREE.Vector3.setFromMatrixPosition( obj.matrixWorld )
	// mesh.position.copy(pos);
	mesh.position.setFromMatrixPosition(obj.matrixWorld);
	mesh.rotation.set(obj.rotation.x, obj.rotation.y, obj.rotation.z);
	mesh.translateZ(-1);
	mesh.scale.set(1.5, 1.5, 1.5);
	return mesh;
}

function render() {
	var time = frame/60;
	renderer.render( scene, camera );
}

function createSkybox() {
	var r = "cube/skybox/";
	var ext = '.jpg';
	var urls = [ r + "px" + ext, r + "nx" + ext,
				 r + "py" + ext, r + "ny" + ext,
				 r + "pz" + ext, r + "nz" + ext ];
	textureCube = new THREE.CubeTextureLoader().load( urls );
	textureCube.format = THREE.RGBFormat;
	textureCube.mapping = THREE.CubeReflectionMapping;
	var textureLoader = new THREE.TextureLoader();
	
	var cubeShader = THREE.ShaderLib[ "cube" ];
	var cubeMaterial = new THREE.ShaderMaterial( {
		fragmentShader: cubeShader.fragmentShader,
		vertexShader: cubeShader.vertexShader,
		uniforms: cubeShader.uniforms,
		depthWrite: false,
		side: THREE.BackSide
	} );
	cubeMaterial.uniforms[ "tCube" ].value = textureCube;
	
	var geo = new THREE.BoxGeometry( 100, 100, 100 )
	cubeMesh = new THREE.Mesh( geo, cubeMaterial );
	scene.add( cubeMesh );
	
}

/*var logo = null;

function createLogo() {
	// instantiate a loader
	var loader = new THREE.OBJLoader();

	// load a resource
	loader.load(
		// resource URL
		'GRANADA.obj',
		// Function when resource is loaded
		function ( object ) {
			object.scale.set(15,15,15);
			object.translateZ(-5);
			object.translateX(-1.5);
			object.rotateX(Math.PI/2);
			scene.add(object);
			logo = object;
		}
	);
}*/

function addGalleryImage(url, angle, vertAngle) {
	var loader = new THREE.TextureLoader();

	// load a resource
	loader.load(
		// resource URL
		url,
		// Function when resource is loaded
		function ( texture ) {
			// do something with the texture
			var material = new THREE.MeshBasicMaterial( {
				map: texture,
				side: THREE.DoubleSide
			 } );
		 	var geometry = new THREE.PlaneGeometry( 2, 2);
		 	// var material = new THREE.MeshBasicMaterial( {color: 0xffffff, side: THREE.DoubleSide} );
		 	var plane = new THREE.Mesh( geometry, material );
		 	plane.rotateY(angle * Math.PI / 180 + Math.PI/2);
			plane.rotateX(vertAngle * Math.PI / 180);
			plane.rotateZ((Math.random() - 0.5) * 2 * Math.PI * 2 * 0.1)
		 	plane.translateZ(-5);
		 	scene.add( plane );
			plane.selectable = true;
		},
		// Function called when download progresses
		function ( xhr ) {
			
		},
		// Function called when download errors
		function ( xhr ) {
			console.log('error')
		}
	);
}

function createText() {
	var loader = new THREE.FontLoader();
	loader.load('droid_serif_regular.typeface.js', function ( font ) {
		var material = new THREE.MultiMaterial( [
							new THREE.MeshPhongMaterial( { color: 0x4444ff, shading: THREE.FlatShading } ), // front
							new THREE.MeshPhongMaterial( { color: 0x4444ff, shading: THREE.SmoothShading } ) // side
						] );
		["NATE", "PARROTT"].forEach(function(text, i) {
			var textGeo = new THREE.TextGeometry(text, {
								font: font,
								size: 0.5,
								height: 0.3,
								material: 0
							});
			textGeo.computeBoundingBox();
			var width = textGeo.boundingBox.max.x - textGeo.boundingBox.min.x;
			var height = textGeo.boundingBox.max.y - textGeo.boundingBox.min.y;
			// var material = new THREE.MeshBasicMaterial( {color: 0xffffff, side: THREE.DoubleSide} );
			var mesh = new THREE.Mesh(textGeo, material);
			mesh.translateX(-width/2)
			mesh.translateY(0.6 - i*0.6 - height/2);
			mesh.translateZ(-4);
			scene.add(mesh);
		});
	} );		
}

function _data_callback(data) {
	var items = data.sections[0];
	items = items.slice(1)
	for (var i=0; i<items.length; i++) {
		var item = items[i];
		var row = i % 2;
		var col = Math.ceil(i/2);
		var nCols = Math.ceil(items.length/2);
		var url = item.style.split('(')[1].split(')')[0];
		var stride = 360 / nCols;
		addGalleryImage(url, (col + row / 2) * stride, row * 40 - 20);
	}
}
