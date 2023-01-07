let tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";

let firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

const songs = [
	'VLsSJyrA1WE',
	'Hkg8uiRadpM',
	'KKGlCPbdnGE',
	'xn7ZEctSYSw',
	'Cy44ocuoWhE',
	'fZgAA0T51Rc',
	'zEv5xrIjIMo',
]
const random = Math.floor(Math.random() * songs.length);

let player;
window.onYouTubeIframeAPIReady = function() {
    player = new YT.Player('player', {
		height: '1',
		width: '1',
		videoId: songs[random],
		suggestedQuality: 'small',
        events: {
            'onReady': onPlayerReady
        }
	})
}

function onPlayerReady(event) {
	$(".loader-wrapper").hide();
	$("#app").css("display", "block");
    event.target.setVolume(50);
}

function pauseVideo() {
    player.pauseVideo();
}

function playVideo() {
	player.playVideo();
}

let volumeUp = $('#volumeUp');
let volumeDown = $('#volumeDown');
$('#pauseplay').on('click', function() {
	if(volumeDown.is(':visible')) {
		volumeDown.hide();
		volumeUp.show();
		playVideo();
	} else {
		volumeUp.hide();
		volumeDown.show();
		pauseVideo();
	}
});
