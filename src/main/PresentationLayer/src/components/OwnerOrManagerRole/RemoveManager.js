import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Form} from 'react-bootstrap'
import * as theService from '../../services/communication';
import { confirmAlert } from 'react-confirm-alert'; 

function RemoveManager(props){
    useEffect(() => {
        setSelectedStore(props.location.store);
        fetchManagersAppointees();
    }, []);

    const [selectedStore, setSelectedStore] = useState("");
    const [subscriberNickname, setSubscriberNickname] = useState("");
    const [managers, setManagers] = useState(["No managers were appointed by you..."]);


    const fetchManagersAppointees = async () => {
        const promise = theService.fetchManagersAppointees(props.location.store);  // goes to communication.js and sends to server
        promise.then((data) => {
            if (data["data"].length > 0){   // if there are owned stores
                setManagers(data["data"]);
                setSubscriberNickname(data["data"][0]);
            }
            else {
                setManagers(["No managers were appointed by you..."])
            }
        });
    };

    const removeManagerHandler = async () =>{
        if(managers[0] === "No managers were appointed by you..."){
            alert("No managers were appointed by you...");
        }
        else{
            const promise = theService.removeManager(selectedStore, subscriberNickname);
            promise.then((data) => {
                // if(data["data"] !== undefined && data["data"]){
                    confirmAlert({
                        title: data["msg"],
                        buttons: [
                            {   label: 'Remove another manager',
                                onClick: () => { // reset the form in order to add another product
                                    // reset feilds
                                    setSelectedStore(selectedStore);
                                    setSubscriberNickname("");
                                    fetchManagersAppointees();
    
                            }},
                            {
                                label: 'Back',
                                onClick: () => {
                                    props.history.push("./owner")
                            }}
                        ]
                    });
                

            });
        }
        
      };

    return (
        <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>
            <h2 style={{marginTop: "2%"}}>{selectedStore} - Remove Store Manager</h2>
            <Form id='form'>
                <div style={{marginLeft: "30%", marginRight: "30%", marginTop: "2%" , border: "1px solid", borderColor: "#CCCCCC"}}>
                    <Form.Group id='form-group' controlId="managers_appointees" onChange={ event => {setSubscriberNickname(event.target.value)}}>
                        <Form.Label id='form-label' style={{marginTop: "2%"}}>Please choose a manager to remove:</Form.Label>
                        <div style={{marginTop: "2%", marginLeft: "3%", marginRight: "3%", marginBottom:"3%"}}>
                            <Form.Control as="select">
                                {managers.map(nickname => (
                                    <option value={nickname}>{nickname}</option>
                                ))}
                            </Form.Control>
                        </div>

                    </Form.Group>
            
                </div>
                <div style={{marginTop:"2%"}}>
                    <Button id='commit-btn' variant="dark"  onClick={removeManagerHandler}>Commit</Button>
                </div>
            </Form>
        </div>

    );
}

export default RemoveManager;