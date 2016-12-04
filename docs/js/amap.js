var map = new AMap.Map('container',{
    resizeEnable: true,
    zoom: 13
});
map.setCity('石家庄市');

var geocoder
AMap.plugin('AMap.Geocoder',function(){
    geocoder = new AMap.Geocoder({
        city: "0311"//城市，默认：“全国”
    });
    map.addControl(geocoder);
});

function getMarker (map, name) {
    geocoder.getLocation(name, function(status,result){
        if(status=='complete'&&result.geocodes.length){
            var marker = new AMap.Marker({
                map: map,
                position: result.geocodes[0].location
            });
            marker.setLabel({//label默认蓝框白底左上角显示，样式className为：amap-marker-label
                offset: new AMap.Pixel(20, 20),//修改label相对于maker的位置
                content: name
            });
            return marker
        }else{
            console.log('获取位置失败', name);
            return
        }
    })
}
function housesToMap (map, houses) {
    var markers = []
    var house
    for (house of houses) {
        var marker = getMarker(map, house.name)
        if (marker){
            markers.push(marker);
        }
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

housesToMap(map, houses)
