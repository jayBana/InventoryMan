// this function is a modified version of
// jdmcnair's code from http://plnkr.co/edit/Ht9pvV?p=info
myApp.filter('dateRange', function () {
    return function (items, start_date, end_date) {
        var result = [];

        // date filters
        var start_date = (start_date && !isNaN(Date.parse(start_date))) ? Date.parse(start_date) : 0;
        var end_date = (end_date && !isNaN(Date.parse(end_date))) ? Date.parse(end_date) : new Date().getTime();


        if (items && items.length > 0) {
            $.each(items, function (index, item) {
                var itemDate = new Date(item.date);

                if (itemDate >= start_date && itemDate <= end_date) {
                    result.push(item);
                }
            });
            return result;
        }
    };
});
