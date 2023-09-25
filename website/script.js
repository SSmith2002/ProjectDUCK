function loadGrid(rows,cols){
    let grid = document.getElementById("grid");

    for(x=0;x<rows;x++){
        for (y=0;y<cols;y++){
            let duck = document.createElement('div');
            duck.classList.add("gridItem");
            let id = "row" + x + "col" + y;
            duck.id = id;

            grid.appendChild(duck);
        }
    }
}

loadGrid(8,8)