function loadGrid(rows,cols){
    let grid = document.getElementById("grid");

    fetch("http://localhost:8350/getDucks").then(function(response) {
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
    
                grid.appendChild(duck);
            }
        }
      });
}

document.body.onmousedown = function(eventData){
    console.log("entered function")
    let popup = document.getElementById("popup");
    let style = getComputedStyle(popup);
    if(eventData.button == 0 && style.display == "block"){
        console.log("entered if")
        popup.style.display = "none";
    }
}

loadGrid(8,8)