import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Form} from 'react-bootstrap'
import * as theService from '../../services/communication';
import { confirmAlert } from 'react-confirm-alert'; 

function RemoveOwner(props){
    useEffect(() => {
        setSelectedStore(props.location.store);
        fetchOwnersAppointees();
    }, []);

    const [selectedStore, setSelectedStore] = useState("");
    const [subscriberNickname, setSubscriberNickname] = useState("");
    const [owners, setOwners] = useState(["No owners were appointed by you..."]);


    const fetchOwnersAppointees = async () => {
        const promise = theService.fetchOwnersAppointees(props.location.store);  // goes to communication.js and sends to server
        promise.then((data) => {
            if (data["data"].length > 0){   // if there are owned stores
                setOwners(data["data"]);
                setSubscriberNickname(data["data"][0]);
            }
            else {
                setOwners(["No owners were appointed by you..."])
            }
        });
    };

    const removeOwnerHandler = () =>{
        if(owners[0] === "No owners were appointed by you..."){
            alert("No owners were appointed by you...");

        }
        else{
            const promise = theService.removeOwner(selectedStore, subscriberNickname);
            promise.then((data) => {
                if(data["data"] !== undefined && data["data"].length > 0 ){
                    confirmAlert({
                        title: data["msg"],
                        message: data['data'].reduce((acc, curr) => acc + "\n" + curr, []), 
                        buttons: [
                            {   label: 'Remove another owner',
                                onClick: () => { // reset the form in order to add another product
                                    // reset feilds
                                    setSelectedStore(selectedStore);
                                    setSubscriberNickname("");
                                    fetchOwnersAppointees();
    
                            }},
                            {
                                label: 'Back',
                                onClick: () => {
                                    props.history.push("./owner")
                            }}
                        ]
                    });
                }
                else {
                    alert(data["msg"]);
                    setOwners(["No owners were appointed by you..."])
                }

                // alert(data["msg"]);
                // alert(data["data"]);
    
                // // reset feilds
                // setSelectedStore(selectedStore);
                // setSubscriberNickname("");
                // fetchOwnersAppointees();
            });
        }
        
      };

    return (
        <div style={{width: props["screenWidth"], height: props["screenHeight"]}}>
            <h2 style={{marginTop: "2%"}}>{selectedStore} - Remove Store Owner</h2>
            <Form id='form'>
                <div style={{marginLeft: "30%", marginRight: "30%", marginTop: "2%" , border: "1px solid", borderColor: "#CCCCCC"}}>
                    <Form.Group id='form-group' controlId="owners_appointees" onChange={ event => {setSubscriberNickname(event.target.value)}}>
                        <Form.Label id='form-label' style={{marginTop: "2%"}}>Please choose a owner to remove:</Form.Label>
                        <div style={{marginTop: "2%", marginLeft: "3%", marginRight: "3%", marginBottom:"3%"}}>
                            <Form.Control as="select">
                                {owners.map(nickname => (
                                    <option value={nickname}>{nickname}</option>
                                ))}
                            </Form.Control>
                        </div>

                    </Form.Group>
            
                </div>
                <div style={{marginTop:"2%"}}>
                    <Button id='commit-btn' variant="dark" onClick={removeOwnerHandler}>Commit</Button>
                </div>
            </Form>
        </div>
    );
}

export default RemoveOwner;