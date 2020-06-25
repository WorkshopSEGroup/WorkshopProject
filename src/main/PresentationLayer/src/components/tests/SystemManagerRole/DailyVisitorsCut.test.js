import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import DailyVisitorsCut from '../../SystemManagerRole/DailyVisitorsCut'


it('renders without crashing', () => {
    shallow(<DailyVisitorsCut />);
  });


describe('DailyVisitorsCut Test Suite', () => {

  // checking if the form elements exist and renders all elements
  it('should render the form', () => {
      const wrapper = shallow(<DailyVisitorsCut />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
      expect(wrapper.find('#container').exists()).toBeDefined();
      expect(wrapper.find('#form').exists()).toBeDefined();
      expect(wrapper.find('#form-label-start').exists()).toBeDefined();
      expect(wrapper.find('#form-label-end').exists()).toBeDefined();
      expect(wrapper.find('#form-start').exists()).toBeDefined();
      expect(wrapper.find('#form-end').exists()).toBeDefined();
      expect(wrapper.find('#open-store-button').exists()).toBeDefined();
      expect(wrapper.find('#chart').exists()).toBeDefined();

  })
});

// describe('Name Test Suite', () => {

//     it('should change the state of the PurchaseProducts component', () => {

//         const wrapper = shallow(<PurchaseProducts />);
//         wrapper.find('#name').simulate('change',
//             {
//                 target: { value: 'some name' }
//             });
//         wrapper.update(); // need to re-render the component to see the changes
//         expect(wrapper.find('#name').prop('value')).toEqual('some name'); // check that state was changed
//     })
// })
