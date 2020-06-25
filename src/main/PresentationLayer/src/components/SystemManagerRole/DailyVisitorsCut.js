import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter as Link } from 'react-router-dom'
import {Container, Button, Form} from 'react-bootstrap'
import * as theService from '../../services/communication';
import { Chart } from "react-google-charts";

function DailyVisitorsCut(props){
    useEffect(() => {
        // setStoreName(props.storeName)
      }, []);


    // const [storeName, setStoreName] = useState("");
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [visitorsCut, setVisitorsCut] = useState([]);
    const [showGraph, setShowGraph] = useState(false);
    const [graphData, setGraphData] = useState(null);
    

    const fetchVisitorsCut = async () =>{
        const promise = theService.getVisitorsCut(startDate, endDate); // goes to register.js and sends to backend
        promise.then((data) => {
            if(data !== undefined){
                if (data["data"] != null && data['data'] !== []){   // if there are stores to display
                    setVisitorsCut(data["data"]);
                    var columns = [['Day', 'Guests', 'Subscribers', 'Store managers', 'Store owners', 'System managers']]
                    // row value example{'date': datetime(2020, 6, 16), 'guests': 3, 'subscribers': 3, 'store_managers': 3, 'store_owners': 3, 'system_managers': 3},
                    var values = data["data"].map(row => [(new Date(row['date'])).toLocaleDateString(), row['guests'], row['subscribers'], row['store_managers'], row['store_owners'], row['system_managers']])

                    setGraphData(columns.concat(values));
                    setShowGraph(true)
                    setStartDate(null)
                    setEndDate(null)

                }
                else{
                    alert(data["msg"])
                    setVisitorsCut(data["data"]);
                }
            }

        });
    };

    
    return (
        <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>

            <div  style={{marginTop:"2%"}}>
                <h1>View Visitors Cut</h1>

                <div style={{marginTop:"2%" , marginLeft: "30%", marginRight: "30%", border: "1px solid", borderColor: "#CCCCCC"}}>
                    <Container id='container'>
                        <h4 style={{marginTop:"2%"}}>Please enter dates range</h4>
                        <Form id='form'>

                            <Form.Label id='form-label-start' style={{marginTop:"2%"}}>Start date:</Form.Label>
                            <Form.Control id='form-start' required type="date" placeholder="Start date" max={(new Date()).toJSON().split('T')[0]} onChange={(event => {setStartDate(event.target.valueAsDate)})}/>
                            <Form.Label id='form-label-end' style={{marginTop:"2%"}}>End date:</Form.Label>
                            <Form.Control id='form-end' required type="date" placeholder="End date" min={(new Date(startDate)).toJSON().split('T')[0]} max={(new Date()).toJSON().split('T')[0]} onChange={(event => {setEndDate(event.target.valueAsDate)})} disabled={startDate === null}/>

                            <Button style={{marginTop:"2%", marginBottom:"2%"}} variant="dark" id="open-store-button" type='reset'
                            //  disabled={startDate === null || endDate === null}
                            onClick={fetchVisitorsCut}>View Cut!</Button>

                        </Form>
                    </Container>
                </div>

                {showGraph ? 
                    <div style={{ tableLayout:'fixed', position:'inherit' }}>
                        <Chart
                            id="chart"
                            width={"100%"}
                            height={"100vh"}
                            chartType="ColumnChart"
                            loader={<div>Loading Chart</div>}
                            data={graphData}
                            // {[['Day', 'Guests', 'Subscribers', 'Store managers', 'Store owners', 'System managers'],
                            //   [(new Date()).toLocaleDateString(), 50, 80,0,1,2],
                            //   [(new Date()).toLocaleDateString(), 50, 80,0,1,2],
                            //   [(new Date()).toLocaleDateString(), 50, 80,0,1,2]
                            // ]}
                           
                            options={{
                                title: 'Daily visitors cut',
                                chartArea: { width: '50%', height: '80%' },
                                position:'inherit',
                                hAxis: {
                                    title: 'Date',
                                    // minValue: (new Date()).toLocaleDateString(),

                                },
                                vAxis: {
                                    title: 'Visitors',
                                },
                                colors: ["rgb(255,178,211)", 'rgb(255,85,171)', "rgb(15,41,144)", "rgb(0,89,196)", "rgb(91,180,233)"],
                                // animation: {
                                //     startup: true,
                                //     easing: 'linear',
                                //     duration: 1000,
                                //   },
                            }}
                            legendToggle
                        /> 
                    </div> 
                : null}
                
            </div>
            
        </div>
    );
 }

export default DailyVisitorsCut;
