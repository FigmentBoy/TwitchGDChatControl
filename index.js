if (require('fs').readFileSync('setup.txt').indexOf('true') != -1) {
    require( "child_process" ).spawnSync( "setup.bat" , { stdio: "inherit", stdin: "inherit" } );
    require('fs').writeFileSync('setup.txt', 'false')
    console.clear()
}
require( "child_process" ).spawnSync( "run.bat" , { stdio: "inherit", stdin: "inherit" } );