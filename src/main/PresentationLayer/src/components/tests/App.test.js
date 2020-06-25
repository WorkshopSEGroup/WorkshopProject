// import React from 'react';
// import { render } from '@testing-library/react';
import React from 'react';
import { shallow, mount, render } from '../../enzyme';
import App from '../../App';

// test('renders learn react link', () => {
//   const { getByText } = render(<App />);
//   // const linkElement = getByText(/learn react/i);
//   // expect(linkElement).toBeInTheDocument();
// });

    
    it('renders without crashing', () => {
      shallow(<App />);
    });


describe('App Test Suite', () => {

    // checking if the form elements exist and renders all elements
    it('should render the form', () => {
        const wrapper = shallow(<App />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
        expect(wrapper.find('#navbar').exists()).toBeDefined();
        expect(wrapper.find('#navbar-logo').exists()).toBeDefined();
        expect(wrapper.find('#navbar-nav').exists()).toBeDefined();
        expect(wrapper.find('#navbar-shopping-cart').exists()).toBeDefined();
        expect(wrapper.find('#form').exists()).toBeDefined();
        expect(wrapper.find('#cart').exists()).toBeDefined();
        expect(wrapper.find('#searchby').exists()).toBeDefined();

        // expect(wrapper.find('#form-dropdown-menu').exists()).toBeDefined();
        // expect(wrapper.find('#form-dropdown-item1').exists()).toBeDefined();
        // expect(wrapper.find('#form-dropdown-item2').exists()).toBeDefined();
        // expect(wrapper.find('#form-dropdown-item3').exists()).toBeDefined();
        // expect(wrapper.find('#form-category-dropdown').exists()).toBeDefined();
        // expect(wrapper.find('#form-search-button').exists()).toBeDefined();
        // expect(wrapper.find('#form-category-dropdown').exists()).toBeDefined();
        // expect(wrapper.find('#form-category-dropdown').exists()).toBeDefined();
        // expect(wrapper.find('#form-category-dropdown').exists()).toBeDefined();
        // expect(wrapper.find('#form-category-dropdown').exists()).toBeDefined();
        // expect(wrapper.find('#form-category-dropdown').exists()).toBeDefined();
        // expect(wrapper.find('#form-search-text').length).toEqual(1);

        
    })
});


// describe('Search field Test Suite', () => {

//   //checking if user name field received the expected input
//     it('should change the state of the App component', () => {

//         const wrapper = shallow(<App />);
//         //simulate the event onChange, which happens once an input is entered
//         wrapper.find('#form-search-text').simulate('change',
//             {
//                 target: {value: 'search text', }
//             });
//         wrapper.update();
//         expect(wrapper.find('#form-search-text').prop('value')).toEqual('search text'); // check that the value of the text field is now set to the input

//   })
// });
