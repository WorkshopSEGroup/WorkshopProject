import React from 'react';
import { shallow, mount, render } from '../../enzyme';
import PersonalPurchaseHistory from '../SubscriberRole/PersonalPurchaseHistory'



    it('renders without crashing', () => {
        shallow(<PersonalPurchaseHistory />);
    });

describe('PersonalPurchaseHistory Test Suite', () => {

    // checking if the form elements exist and renders all elements
    it('should render the form', () => {
        const wrapper = shallow(<PersonalPurchaseHistory />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.


    })
});