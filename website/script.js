function loadGrid(rows,cols){
    let grid = document.getElementById("grid");

    fetch("http://192.168.1.211:8350/getDucks").then(function(response) {
        return response.text();
      }).then(function(data) {
        for(x=0;x<rows;x++){
            for (y=0;y<cols;y++){
                let duck = document.createElement('div');
                duck.classList.add("gridItem");

                duckNumber = (x*8) + y
                if(data[duckNumber] == 1){
                    duck.classList.add("found");
                }
                else{
                    duck.classList.add("notFound");
                }
                let id = "row" + x + "col" + y;
                duck.id = id;
                duck.innerHTML = duckNumber + 1
    
                grid.appendChild(duck);
            }
        }
      });
}

document.body.onmousedown = function(eventData){
    let popup = document.getElementById("popup");
    let style = getComputedStyle(popup); 
    if(eventData.button == 0 && style.display == "block"){
        popup.style.display = "none";
    }
}

loadGrid(8,8)