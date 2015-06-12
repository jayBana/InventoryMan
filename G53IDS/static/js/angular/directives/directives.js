myApp.directive('myDatePicker', [function () {
    return {
        restrict: 'E',
        templateUrl: '../../static/partials/datepicker.html',
        controller: function () {
            $(' .input-daterange').datepicker({
                format: "yyyy-mm-dd",
                weekStart: 1,
                startDate: "+1d",
                endDate: "+14d"
            });
        },
        link: function ($scope, $element, $attrs) {
            $('#start').on("change", function(e) {
                $scope.$apply(function(){
                    $scope.start_date = $('#start').val();
                });
            });
            $('#end').on("change", function(e) {
               $scope.$apply(function() {
                    $scope.end_date = $('#end').val();
                });
            });
        }
    }
}]);