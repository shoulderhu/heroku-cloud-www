$(document).ready(function() {

    let toggle = $("#toggle");
    let select = $(".selectpicker");
    let chart = new Chart($("#chart"), {
        type: "line",
        data: {
            labels: [],
            datasets: []
        },
        options: {
            legend: {
                labels: {
                    usePointStyle: true
                }
            }
        }
    });

    let g = "rgb(0, 232, 0)";
    let y = "rgb(255, 255, 0)";
    let o = "rgb(255, 126, 0)";
    let r = "rgb(255, 0, 0)";
    let p = "rgb(143, 63, 151)";
    let b = "rgb(126, 0, 35)";
    let t = "rgba(0, 0, 0, 0)";

    $("select").on("changed.bs.select", function(e, clickedIndex, newValue, oldValue) {
        //console.log(this.value, clickedIndex, newValue, oldValue)
        //console.log($("ul#tab a.active").attr("id"))
        Update();
    });

    $('a[data-toggle="tab"]').on("shown.bs.tab", function(e) {
        let id = $(e.target).attr("id");
        //alert(target);
        //console.log(target);
        //labels.push(Math.floor(Math.random() *100) + 1);
        //labels = data2;
        //data = data2;

        Update();
    });

    toggle.bootstrapToggle("on");
    toggle.change(function() {

        let checked = $(this).prop("checked");

        chart.data.datasets.forEach(function(dataset) {

            dataset.hidden = !checked;
        });

        chart.update();
    });

    function Update() {

        let tab = $("ul#tab a.active").attr("id");
        let checked = toggle.prop("checked");

        select.attr("disabled", true);
        select.selectpicker('refresh');

        toggle.prop("disabled", true).change();

        $.post("http://114.32.4.146:5000/api/aqi", {"tab": tab,
            "date": $("#日期").val(), "zone": $("#空品區").val()}, function(res) {

            chart.data.labels = res["labels"];
            chart.data.datasets = [];

            for(let i = 0; i < res["data"].length; ++i) {

                let data = res["data"][i];

                chart.data.datasets.push({
                    label: res["label"][i],
                    data: res["data"][i],
                    fill: false,
                    hidden: !checked,
                    borderColor: randomColor(),
                    backgroundColor: aqiColor(tab, res["data"][i])
                });
            }

            chart.update();
            select.removeAttr("disabled");
            select.selectpicker('refresh');
            toggle.prop("disabled", false).change();
        });
    }

    function randomColor() {

        let r = Math.floor(Math.random() * 255);
        let g = Math.floor(Math.random() * 255);
        let b = Math.floor(Math.random() * 255);
        return "rgb(" + r + "," + g + "," + b + ")";
    }

    function aqiColor(tab, data) {

        color = [];

        for(let i = 0; i < data.length; ++i) {

            color.push(AQI(data[i]));
        }

        return color;
    }

    function AQI(ugm3) {

         if (0 <= ugm3 && ugm3 <= 50) {
            return g;
        }
        else if (51 <= ugm3 && ugm3 <= 100) {
            return y;
        }
        else if (101 <= ugm3 && ugm3 <= 150) {
            return o;
        }
        else if (151 <= ugm3 && ugm3 <= 200) {
            return r;
        }
        else if (201 <= ugm3 && ugm3 <= 300) {
            return p;
        }
        else if(301 <= ugm3 && ugm3 <= 500) {
            return b;
        }
        else { return t; }

    }

    Update();
});