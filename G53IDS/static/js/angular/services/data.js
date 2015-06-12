// service for getting the data from the service,
// based on the principle of the promise object
myApp.factory("Data", ['$http',
    function ($http, $q) {
        var obj = {};
        var pathBase = '/';
        obj.get = function (q) {
            return $http.get(pathBase + q).then(function (results) {
                return results.data;
            });
        };
        return obj;
    }]);