class Floor {
    constructor(startConnector, endConnector, distance) {
        this.startConnector = startConnector;
        this.endConnector = endConnector;
        this.distance = distance;
        this.temp = [];
    }

    highlight(point) {
        for (let index = 0; index < this.temp.length; index++) {
            document.getElementById(this.temp[index]).style.backgroundColor = "#474344";
        }

        this.temp = [];
        document.getElementById(point).style.backgroundColor = "#22329e";
        this.temp.push(point);
        for (let index = 0; index < this.startConnector.length; index++) {
            if (this.startConnector[index] == point) {
                document.getElementById(this.endConnector[index]).style.backgroundColor = "#F37F7F";
                this.temp.push(this.endConnector[index]);
            }
        }
    } 
}

// class Point {
//     constructor(point1, point2, distance) {
//         this.point1 = point1;
//         this.point2 = point2;
//         this.distance = distance;
//         this.temp = [];
//     }

//     highlight(point) {
//         for (let index = 0; index < this.temp.length; index++) {

//         }
//     }
// }