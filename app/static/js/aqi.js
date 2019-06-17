$(document).ready(function() {

    let toggle = $("#toggle");
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

    toggle.bootstrapToggle("on");
    toggle.change(function() {

        let checked = $(this).prop("checked");

        chart.data.datasets.forEach(function(dataset) {

            dataset.hidden = !checked;
        });
        chart.update();
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

    Update();

    function Update() {

        let tab = $("ul#tab a.active").attr("id");
        let checked = toggle.prop("checked");

        $.post("https://cloud-www.herokuapp.com/api/aqi", {"tab": tab,
            "date": $("#日期").val(), "zone": $("#空品區").val()}, function(res) {

            chart.data.labels = res["labels"];
            chart.data.datasets = [];

            for(let i = 0; i < res["data"].length; ++i) {

                let data = res["data"][i];

                if(tab === "o3-tab" || tab === "o3-8-tab") {

                    for(let j = 0; j < data.length; ++j) {

                        data[j] /= 1000;
                    }
                }

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

        switch (tab) {
            case "o3-8-tab":
                for(let i = 0; i < data.length; ++i) {

                    color.push(O3_8(data[i]));
                }
                break;
            case "o3-tab":
                for(let i = 0; i < data.length; ++i) {

                    color.push(O3(data[i]));
                }
                break;
            case "pm25-tab":
                for(let i = 0; i < data.length; ++i) {

                    color.push(PM25(data[i]));
                }
                break;
            case "pm10-tab":
                for(let i = 0; i < data.length; ++i) {

                    color.push(PM10(data[i]));
                }
                break;
            case "co-tab":
                for(let i = 0; i < data.length; ++i) {

                    color.push(CO(data[i]));
                }
                break;
            case "so2-tab":
                for(let i = 0; i < data.length; ++i) {

                    color.push(SO2(data[i]));
                }
                break;
            case "no2-tab":
                for(let i = 0; i < data.length; ++i) {

                    color.push(NO2(data[i]));
                }
                break;
        }

        return color;
    }

    function O3_8(ppm) {

        if(0 <= ppm && ppm <= 0.054) {
            return g;
        }
        else if (0.055 <= ppm && ppm <= 0.070) {
            return y;
        }
        else if (0.071 <= ppm && ppm <= 0.085) {
            return o;
        }
        else if (0.086 <= ppm && ppm <= 0.105) {
            return r;
        }
        else if (0.106 <= ppm && ppm <= 0.2) {
            return p;
        }
        else { return t; }
    }

    function O3(ppm) {

        if (0.125 <= ppm && ppm <= 0.164) {
            return o;
        }
        else if (0.165 <= ppm && ppm <= 0.204) {
            return r;
        }
        else if (0.205 <= ppm && ppm <= 0.404) {
            return p;
        }
        else if (0.405 <= ppm && ppm <= 0.604) {
            return b;
        }
        else { return t; }
    }

    function PM25(ugm3) {

        if (0 <= ugm3 && ugm3 <= 15.4) {
            return g;
        }
        else if (15.5 <= ugm3 && ugm3 <= 35.4) {
            return y;
        }
        else if (35.5 <= ugm3 && ugm3 <= 54.4) {
            return o;
        }
        else if (54.5 <= ugm3 && ugm3 <= 150.4) {
            return r;
        }
        else if (150.5 <= ugm3 && ugm3 <= 250.4) {
            return p;
        }
        else if(250.5 <= ugm3 && ugm3 <= 500.4) {
            return b;
        }
        else { return t; }
    }

    function PM10(ugm3) {

        if (0 <= ugm3 && ugm3 <= 54) {
            return g;
        }
        else if (55 <= ugm3 && ugm3 <= 125) {
            return y;
        }
        else if (126 <= ugm3 && ugm3 <= 254) {
            return o;
        }
        else if (255 <= ugm3 && ugm3 <= 354) {
            return r;
        }
        else if (355 <= ugm3 && ugm3 <= 424) {
            return p;
        }
        else if(425 <= ugm3 && ugm3 <= 604) {
            return b;
        }
        else { return t; }
    }

    function CO(ppm) {

        if(0 <= ppm && ppm <= 4.4) {
            return g;
        }
        else if (4.5 <= ppm && ppm <= 9.4) {
            return y;
        }
        else if (9.5 <= ppm && ppm <= 12.4) {
            return o;
        }
        else if (12.5 <= ppm && ppm <= 15.4) {
            return r;
        }
        else if (15.5 <= ppm && ppm <= 30.4) {
            return p;
        }
        else if (30.5 <= ppm && ppm <= 50.4) {
            return p;
        }
        else { return t; }
    }

    function NO2(ppb) {

        if (0 <= ppb && ppb <= 53) {
            return g;
        }
        else if (54 <= ppb && ppb <= 100) {
            return y;
        }
        else if (101 <= ppb && ppb <= 360) {
            return o;
        }
        else if (361 <= ppb && ppb <= 649) {
            return r;
        }
        else if (650 <= ppb && ppb <= 1249) {
            return p;
        }
        else if(1250 <= ppb && ppb <= 2049) {
            return b;
        }
        else { return t; }
    }

    function SO2(ppb) {

        if (0 <= ppb && ppb <= 35) {
            return g;
        }
        else if (36 <= ppb && ppb <= 75) {
            return y;
        }
        else if (76 <= ppb && ppb <= 185) {
            return o;
        }
        else if (186 <= ppb && ppb <= 304) {
            return r;
        }
        else if (305 <= ppb && ppb <= 604) {
            return p;
        }
        else if (605 <= ppb && ppb <= 1004) {
            return b;
        }
        else { return t; }
    }
});