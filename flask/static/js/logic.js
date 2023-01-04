



data = eps_data;

// creating select options for the search box
for (var i = 0; i <data.length; i++ )

Object.entries(data[i]).forEach(([key,value]) =>
{
    if (key == "Ticker")
    {
        var txtVal = value;
        liNode = document.createElement("option");
        listNode = document.getElementById("ddselect")
        txtNode = document.createTextNode(txtVal);
    liNode.appendChild(txtNode);
    listNode.appendChild(liNode);


    }


} )

// bootstrap search box 
$(document).ready(function()
{
$('.search_select_box select').selectpicker();
});

// bootstrap navbar search box
$(document).ready(function()
    {
        $('.selectpicker select').selectpicker();
    }
);


function updatePage()
{
    var dropdownMenu = d3.selectAll("#ddselect").node();
    Ticker = dropdownMenu.value;
    console.log(dropdownMenu);
    console.log("hello")
    console.log(Ticker);
    // const dict_values = {Ticker};
    const dict_values = {"Ticker": Ticker} 
    console.log(dict_values);
    const s = JSON.stringify(dict_values);
    console.log(s);;

    $(document).ready(function() {
          $.ajax({
            data :JSON.stringify(dict_values),
            //data: dict_values,
            type : 'POST',
            url : '/StockAnalysis',
            contentType: 'application/json'
          });
      });

      // update the display 
      const name = document.querySelector(".name");
      name.innerText = Ticker;

    //   prices = "129"

    //   const price = document.querySelector(".current_price")
    //   price.innerText = prices;
    
}

function myFunc(vars)
{
    console.log(vars)
    return vars
}

// let list_data = {{input_from_python | tojson}};


d3.selectAll(".search_select_box").on("change", updatePage);
// d3.selectAll(".search_select_box").on("change", server.ticker());
