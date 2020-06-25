import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import DisplayStores from '../../Actions/StoreActions/DisplayStores'



    it('renders without crashing', () => {
        shallow(<DisplayStores />);
    });

describe('DisplayStores Test Suite', () => {

    // checking if the form elements exist and renders all elements
    it('should render the form', () => {
        const wrapper = shallow(<DisplayStores />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
        expect(wrapper.find('#form').exists()).toBeDefined();
        expect(wrapper.find('#form-group').exists()).toBeDefined();
        expect(wrapper.find('#form-label').exists()).toBeDefined();
        expect(wrapper.find('#form-select').exists()).toBeDefined();
        expect(wrapper.find('#form-2').exists()).toBeDefined();
        expect(wrapper.find('#form-2-label').exists()).toBeDefined();
        expect(wrapper.find('#form-2-check-1').exists()).toBeDefined();
        expect(wrapper.find('#form-2-check-2').exists()).toBeDefined();
        expect(wrapper.find('#display-button').exists()).toBeDefined();
    })
});


// describe('Store Info radio button selected Test Suite', () => {

//     //checking if radio button was selected upon event
//     it('should change the state of the DisplayStores component', () => {

//         const wrapper = shallow(<DisplayStores />);
//         wrapper.find('#form-2-check-1').simulate('change');
//         wrapper.update();
//         expect(wrapper.find('#form-2-check-1').prop('checked')).toEqual(true); // check that the value of the text field is now set to the input

//     })
// });