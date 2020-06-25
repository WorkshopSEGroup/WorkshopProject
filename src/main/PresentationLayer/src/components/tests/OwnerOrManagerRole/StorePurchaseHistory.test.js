import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import StorePurchaseHistory from '../../OwnerOrManagerRole/StorePurchaseHistory'


it('renders without crashing', () => {
    shallow(<StorePurchaseHistory />);
  });


describe('systemManagerAPI Test Suite', () => {

  it('should render the form', () => {
      const wrapper = shallow(<StorePurchaseHistory />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
      expect(wrapper.find('#table').exists()).toBeDefined();
      expect(wrapper.find('#form').exists()).toBeDefined();
      
  })
});