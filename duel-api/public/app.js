angular.module('duelApp', [])
    .controller('MainCtrl', function($scope, $http, $timeout) {

        const AVAILABLE_PAGES = ["overview", "programs", "advocates"]

        var vm = this
        vm.current_page = "overview"
        vm.overview_data = {}
        vm.platforms = []
        vm.platform_data_loaded = false
        vm.platorm_data = {}
        vm.combined_platform_data = {}

        vm.selected_outcome = "likes"


        vm.init = function() {
            $http.get('/api/overview').then(function(response) {
                vm.overview_data = response.data;
            });

            $http.get('/api/platforms').then(function(response) {
                vm.platforms = response.data;
                for (let platform of vm.platforms) {
                    $http.get('/api/stats/platform/' + platform.platform).then(function(response) {
                        vm.platorm_data[platform.platform] = response.data;
                        if (Object.keys(vm.platorm_data).length === vm.platforms.length) {
                            vm.combined_platform_data = combine_platform_data();
                            vm.platform_data_loaded = true;
                            $timeout(function() {
                                vm.show_performance_graph('likes');
                            }, 500);
                        }
                    });
                }

            });
        }


        function combine_platform_data() {
            platform_data = {
                labels: [],
                activities: [],
                likes: [],
                comments: [],
                reach: [],
                shares: [],
                total_sales_attributed: [],
            }
            for (const platformObj of vm.platforms) {
                const platform = platformObj.platform;
                platform_data['labels'].push(platform);
                const platformData = vm.platorm_data[platform];
                console.log(vm.platorm_data)
                if (platformData && platformData.data && platformData.data[0]) {
                    platform_data['likes'].push(platformData.data[0].total_likes);
                    platform_data['comments'].push(platformData.data[0].total_comments);
                    platform_data['activities'].push(platformData.data[0].activities);
                    platform_data['comments'].push(platformData.data[0].total_comments);
                    platform_data['reach'].push(platformData.data[0].total_reach);
                    platform_data['shares'].push(platformData.data[0].total_shares);
                    platform_data['total_sales_attributed'].push(platformData.data[0].total_sales_attributed);
                } else {
                    platform_data['likes'].push(0);
                    platform_data['comments'].push(0);
                    platform_data['activities'].push(0);
                    platform_data['comments'].push(0);
                    platform_data['reach'].push(0);
                    platform_data['shares'].push(0);
                    platform_data['total_sales_attributed'].push(0);
                }
            }

            return platform_data
        }


        vm.switch_page = function(page) {
            if (AVAILABLE_PAGES.includes(page)) {
                vm.current_page = page
            } else { vm.current_page = "overview" }

            if (page === "overview") {

            }
        }

        vm.show_performance_graph = function(series) {
            vm.selected_outcome = series;
            show_graph (vm.combined_platform_data['labels'], vm.combined_platform_data[series], series)
        }




    });
