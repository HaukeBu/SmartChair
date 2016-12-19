import {Component, ViewChild, ElementRef} from '@angular/core';
import * as io from "socket.io-client";

@Component({
    selector: 'pressure',
    template: `
        <canvas class="canvas" #pressureCanvas width="150" height="300"></canvas>
        <img #source src="https://mdn.mozillademos.org/files/5397/rhino.jpg"
           width="300" height="227">
    `,
    styles: [`
        .canvas {
          border: 1px solid black;
          padding-left: 15px;
          padding-right: 15px;
        }
        img {
            display: none;
        }
    `]
})

export class PressureComponent {

    pressure = {};
    socket:any = null;
    drawReady = false;

    @ViewChild("pressureCanvas") pressureCanvas: ElementRef;

    constructor() {
        for(var i = 0; i < 10; i++) {
            this.pressure[i] = ''+i;
        }

        this.socket = io('http://localhost:8000');
        this.socket.emit('connect', 'hi');

        this.socket.on('message', function(message){
            this.socket.emit('message', 'Hello Server, Im fine');
            console.log(message);
        }.bind(this));

        this.socket.on('pressure', function(message) {
            this.updatePressure(JSON.parse(message));
        }.bind(this));
    }

    updatePressure(pressureJSON): void {
        for(var i in pressureJSON.p) {
            this.pressure[i] = pressureJSON.p[i];
        }
        if(this.drawReady) {
            this.drawCanvasPressure();
        }
    }

    //draw code
    ngAfterViewInit() {
        this.drawReady = true;
    }

    drawCanvasPressure(): void {
        let ctx: CanvasRenderingContext2D = this.pressureCanvas.nativeElement.getContext("2d");
        //some variables to scale context correctly to canvas
        ctx.canvas.height = 2*ctx.canvas.width; //keep ratio to 2:3
        var disY = ctx.canvas.height / 6;
        var disX = ctx.canvas.width / 3;
        var radius = (disY > disX ? disX : disY) / 3;

        ctx.lineWidth = 1;
        ctx.strokeStyle = '#000000';

        //draw chair outlines
        drawRoundRect(disX/2,disY/2,2*disX,3*disY,radius);
        drawRoundRect(disX/2,3*disY+disY/2,2*disX,2*disY,radius);
        drawRoundRect(0,3*disY+disY/2,disX/2,1.8*disY,radius);
        drawRoundRect(ctx.canvas.width-disX/2,3*disY+disY/2,disX/2,1.8*disY,radius);

        drawCircle(1, 1, this.pressure[4]);
        drawCircle(2, 1, this.pressure[5]);
        drawCircle(1, 2, this.pressure[6]);
        drawCircle(2, 2, this.pressure[7]);
        drawCircle(1, 3, this.pressure[8]);
        drawCircle(2, 3, this.pressure[9]);
        drawCircle(1, 4, this.pressure[0]);
        drawCircle(2, 4, this.pressure[1]);
        drawCircle(1, 5, this.pressure[2]);
        drawCircle(2, 5, this.pressure[3]);

        function drawRoundRect(x, y, w, h, r) {
            if (w < 2 * r) r = w / 2;
            if (h < 2 * r) r = h / 2;
            ctx.beginPath();
            ctx.moveTo(x+r, y);
            ctx.arcTo(x+w, y,   x+w, y+h, r);
            ctx.arcTo(x+w, y+h, x,   y+h, r);
            ctx.arcTo(x,   y+h, x,   y,   r);
            ctx.arcTo(x,   y,   x+w, y,   r);
            ctx.closePath();
            ctx.stroke();
        }

        function drawCircle(posX, posY, color) {
            ctx.beginPath();
            ctx.arc(posX * disX, posY * disY, radius, 0, 2*Math.PI);
            ctx.fillStyle = percentageToHsl(color, 120, 0);
            ctx.fill();
            ctx.stroke();
        }

        /**
         * converts a percentage to a HSL color
         * @param percentage: the percentage value as a float between 0 and 1
         * @param hue0: color at 0%
         * @param hue1: color at 100%
         * @returns {string}: returns the string for a HSL-color
         */
        function percentageToHsl(percentage, hue0, hue1) {
            var hue = (percentage * (hue1 - hue0)) + hue0;
            return 'hsl(' + hue + ', 100%, 50%)';
        }
    }
}