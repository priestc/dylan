function set_player(track) {
    // set the player to the track.
    player.attr('src', urls[track]);
    player.attr('track', track);
    set_currently_playing(track);
    player.trigger('change');
}

function get_info(track) {
    // given a track number, return all the data for that track.
    return {
        song: $('#info_' + track + ' .title').text(),
        slug: $('#info_' + track + ' .slug').text(),
        duration: slug = $('#info_' + track + ' .duration').text(),
        album: $('#album_title').text(),
    }
}

function fire_tracking_event(event, track) {
    var info = get_info(track);
    var full_title = info['song'] + ' - ' + info['album']
    //console.log(event, track);
    if(event == 'error') {
        _gaq.push(['_trackEvent', 'error', info['slug']]);
    } else {
        _gaq.push(['_trackEvent', event + '-by-slug', info['slug']]);
        _gaq.push(['_trackEvent', event + '-by-track', full_title]);
    }
}

function set_currently_playing(track) {
    // set the title at the top of the player.
    var data = get_info(track);
    $('#currently_playing').text(data.song + ' [' + data.duration + ']');
    $('#playlist_table tr').removeClass('now_playing');
    $('#playlist_table tr.row_' + track).addClass('now_playing');
}