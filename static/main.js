

function getLastheight(parent,content){
	var container = document.getElementById(parent);
	var childers = container.getElementsByClassName(content);
	var lastHeight = childers[childers.length-1].offsetTop;	
	return lastHeight;
}

function imgLotion(parent,content){
	
	var container = document.getElementById(parent);
	var childers = container.getElementsByClassName(content);
	var imgwidth = childers[0].offsetWidth;
	var cols = Math.floor(document.documentElement.clientWidth/imgwidth);
	container.style.cssText = "width:"+imgwidth*cols+"px; margin:0px auto;";
	var boxheigthArr = [];
	var lastHeight;
	for (var i = 0; i<childers.length;i++) {
		if(i<cols){
			boxheigthArr[i] = childers[i].offsetHeight;
		}else{
			var minHeight = Math.min.apply(null,boxheigthArr);
			//console.log(minHeight);
			var minIndex = getminIndex(boxheigthArr,minHeight);
			//console.log(minIndex);
			childers[i].style.position = "absolute";
			childers[i].style.top = minHeight+"px";
			childers[i].style.left = minIndex*imgwidth+"px";
			//console.log(minIndex*imgwidth);
			boxheigthArr[minIndex] = minHeight + childers[i].offsetHeight;
			lastHeight = boxheigthArr[minIndex];
			//console.log(lastHeight);
		}
	}
	// console.log("最后高度"+lastHeight);
	//return lastHeight;
}

function getminIndex(boxheigthArr,minHeight){
	for (var i = 0 ;i<boxheigthArr.length;i++) {
		if(boxheigthArr[i] == minHeight){
			//console.log("---------------"+i);
			return i;
		}
	}
}
