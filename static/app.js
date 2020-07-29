var url = "http://127.0.0.1:5000/json";
var houseData;

d3.json(url).then(function(houseData){

    var houseData = houseData;
    var city = houseData.map(each=>each.city);
    var uniqueCity = removeDuplicates(city);
    var bed = houseData.map(each=>each.beds);
    var uniqueBed = removeDuplicates(bed);
    var tbody= d3.select("tbody");
    // construct default dropdown menu
    var dropdownMenuCity = d3.select("#city");
    var dropdownMenuBed = d3.select("#beds");

    // construct dataset
    houseData.forEach(eachDict=>{
        processTable(eachDict);
    });

    // append city and beds dropdown menu
    constructOption(dropdownMenuCity,uniqueCity);
    constructOption(dropdownMenuBed,uniqueBed);

    // create event listener for dropdown
    dropdownMenuCity.on("change",getData);
    dropdownMenuBed.on("change",getData);


    /******************************************** Functions *********************************************/
    //----------------------------------------------------------------------------------------------------
    function getData(){
        d3.event.preventDefault();
        
        var cityValue = d3.select("#city").property("value");
        var bedValue = d3.select("#beds").property("value");
        var filteredCityData = houseData.filter(eachRow=> eachRow.city===cityValue);
        var filteredBedData = houseData.filter(eachRow=> eachRow.beds===bedValue);
        var filteredBoth = houseData.filter(eachRow=> eachRow.beds===bedValue && eachRow.city===cityValue);

        // reconstruct table based on the filter
        if(cityValue=="All" && bedValue!=="All"){
            // when select bed value, reconstruct city dropdown options
            var tempCity = removeDuplicates(filteredBedData.map(city=>city.city));
            constructOption(dropdownMenuCity,tempCity);
            outputTable(bedValue,filteredBedData);
        }else if (bedValue=="All" && cityValue!=="All"){
            // when city is selected, reconstruct bed dropdown options
            var tempBed = removeDuplicates(filteredCityData.map(city=>city.beds));
            constructOption(dropdownMenuBed,tempBed);
            outputTable(cityValue,filteredCityData);
        }else{
            outputTable(cityValue,filteredBoth);
        };
        
    
    };

    function outputTable(dropdownValue,dataTable){
        /* reconstruct table based on filter value*/
        // remove existing table
        console.log(dropdownValue)
        tbody.html("");
        if (dropdownValue=="All"){
            houseData.forEach(eachRow=>{processTable(eachRow)});
        }else{
            dataTable.forEach(eachRow=>{processTable(eachRow)});
        };
    };
    
    
    function removeDuplicates(array){
        /* remove duplicates in a array */
        return array.filter((value, index)=> array.indexOf(value)===index);
    }
    
    
    function constructOption(optionName, array){
        /* construct dropdown option based on unique array*/
        optionName.html("");
        optionName.append("option").text("All").attr("name","All").attr("selected","selected");
        array.forEach(city=>{
            optionName.append("option").text(city).attr("name",city);
        });
    
    }
    
    function processTable(tableRow){
        /* construct table based on json data */
        var row = tbody.append("tr");
        Object.entries(tableRow).forEach(([key,value])=>{
            row.append("td").text(value)
        });
    
    };
    



    

});


