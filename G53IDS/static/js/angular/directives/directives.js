myApp.directive('myDatePicker', [function () {
    return {
        restrict: 'E',
        templateUrl: '../../static/partials/datepicker.html',
        controller: function () {
            // Settings of datepicker
            $(' .input-daterange').datepicker({
                format: "yyyy-mm-dd",
                weekStart: 1,
                startDate: "+1d",
                endDate: "+14d"
            });
        },
        // function that can invoke the controller to change
        // the model, when there is change in the view
        link: function ($scope, $element, $attrs) {
            // listen for input changes in the datepicker
            // and update variables in model's scope accordingly
            // this will triger the filtering of rows
            $('#start').on("change", function (e) {
                $scope.$apply(function () {
                    $scope.start_date = $('#start').val();
                });
            });
            $('#end').on("change", function (e) {
                $scope.$apply(function () {
                    $scope.end_date = $('#end').val();
                });
            });
        }
    }
}]);