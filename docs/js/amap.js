var map = new AMap.Map('container',{
    resizeEnable: true,
    zoom: 13
});
map.setCity('石家庄市');

var geocoder
AMap.plugin(['AMap.ToolBar', 'AMap.Geocoder'],function(){
    geocoder = new AMap.Geocoder({
        city: "0311"//城市，默认：“全国”
    });
    map.addControl(new AMap.ToolBar());
    map.addControl(geocoder);
});

function getMarker (map, house, markers) {
    var name = house.name;
    geocoder.getLocation(name, function(status,result){
        if(status=='complete'&&result.geocodes.length){
            var marker = new AMap.Marker({
                map: map,
                position: result.geocodes[0].location
            });
            marker.house = house
            marker.setLabel({//label默认蓝框白底左上角显示，样式className为：amap-marker-label
                offset: new AMap.Pixel(20, 20),//修改label相对于maker的位置
                content: name
            });
            markers.push(marker);

            return marker
        }else{
            console.log('获取位置失败', name);
            return
        }
    })
}
var markers = []
function housesToMap (map, houses) {
    markers = []
    var house
    for (house of houses) {
        getMarker(map, house, markers)
    }
}

// houses 数据格式
// var houses = [{
//     'price': '价格待定',
//     'time': '201701.htm',
//     'area': '[栾城]',
//     'houseType': '2居/3居－78~137平米',
//     'name': '蓝郡国际'
// }]

function load () {
    housesToMap(map, houses)
}

function filterHouses () {
    var time = document.getElementById("form-time").value

    var newMarkers = markers
    if (time) {
        newMarkers = markers.filter(function (marker) {
            return marker.house.time.startsWith(time)
        });
    }
    var oldMarker = map.getAllOverlays("marker");
    map.remove(oldMarker);
    map.add(newMarkers)
    console.log("找到数量：", newMarkers.length , " 关键字：", time);
    return false;
}
