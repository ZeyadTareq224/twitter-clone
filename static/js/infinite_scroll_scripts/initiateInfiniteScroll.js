var infinite = new Waypoint.Infinite({
            element: $('.infinite-container')[0],

            offset: 'bottom-in-view',

            onBeforePageLoad: function () {
                $('.loading').show();
            },
            onAfterPageLoad: function () {
                $('.loading').hide();
            }

        });