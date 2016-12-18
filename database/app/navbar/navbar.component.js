/**
 * Created by Kounex on 21.11.16.
 */
"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var chair_service_1 = require('../shared/chair.service');
var chair_1 = require("../shared/chair");
var NavbarComponent = (function () {
    function NavbarComponent(chairService) {
        this.chairService = chairService;
        this.title = 'Smart Chair';
        this.chairs = [];
    }
    NavbarComponent.prototype.getChairs = function () {
        var _this = this;
        this.connection = this.chairService.getChairs().subscribe(function (chairs) {
            var chairJSON = JSON.parse('' + chairs);
            for (var i in chairJSON.cid) {
                _this.chairs[i] = new chair_1.Chair(chairJSON.cid[i]);
            }
        });
    };
    NavbarComponent.prototype.ngOnInit = function () {
        this.getChairs();
    };
    NavbarComponent = __decorate([
        core_1.Component({
            selector: 'navbar',
            templateUrl: './app/navbar/navbar.component.html',
            providers: [chair_service_1.ChairService]
        }), 
        __metadata('design:paramtypes', [chair_service_1.ChairService])
    ], NavbarComponent);
    return NavbarComponent;
}());
exports.NavbarComponent = NavbarComponent;
//# sourceMappingURL=navbar.component.js.map