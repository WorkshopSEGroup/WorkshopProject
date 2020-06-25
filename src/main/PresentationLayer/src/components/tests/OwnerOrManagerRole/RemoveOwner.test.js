import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import RemoveOwner from '../../OwnerOrManagerRole/RemoveOwner'


it('renders without crashing', () => {
    shallow(<RemoveOwner />);
  });


describe('systemManagerAPI Test Suite', () => {

  it('should render the form', () => {
      const wrapper = shallow(<RemoveOwner />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
      expect(wrapper.find('#form').exists()).toBeDefined();
      expect(wrapper.find('#form-group').exists()).toBeDefined();
      expect(wrapper.find('#form-label').exists()).toBeDefined();
    //   expect(wrapper.find('#form-select').exists()).toBeDefined();
      expect(wrapper.find('#commit-btn').exists()).toBeDefined();
      
  })
});