let tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";

let firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

let player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
		height: '1',
		width: '1',
		videoId: 'VLsSJyrA1WE',
		suggestedQuality: 'small',
        events: {
            'onReady': onPlayerReady
        }
	})
}

function onPlayerReady(event) {
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