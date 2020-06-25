import React from 'react';
import { shallow, mount, render } from '../../../enzyme';
import ManageStorePolicies from '../../OwnerOrManagerRole/ManageStorePolicies'


it('renders without crashing', () => {
    shallow(<ManageStorePolicies />);
  });


describe('systemManagerAPI Test Suite', () => {

  it('should render the form', () => {
      const wrapper = shallow(<ManageStorePolicies />);  // shallow renders a single component each time. In other words, Enzyme won’t consider the child elements for the test.
      expect(wrapper.find('#accordion').exists()).toBeDefined();
      expect(wrapper.find('#card').exists()).toBeDefined();
      expect(wrapper.find('#accordion-toggle').exists()).toBeDefined();
      expect(wrapper.find('#container').exists()).toBeDefined();
      expect(wrapper.find('#form').exists()).toBeDefined();
      expect(wrapper.find('#Radios1').exists()).toBeDefined();
      expect(wrapper.find('#Radios2').exists()).toBeDefined();
      expect(wrapper.find('#Radios3').exists()).toBeDefined();
      expect(wrapper.find('#Radio4').exists()).toBeDefined();
      expect(wrapper.find('#card-2').exists()).toBeDefined();
      expect(wrapper.find('#accordion-toggle-2').exists()).toBeDefined();
      expect(wrapper.find('#container-2').exists()).toBeDefined();
      expect(wrapper.find('#form-2').exists()).toBeDefined();
      expect(wrapper.find('#Radios5').exists()).toBeDefined();
      expect(wrapper.find('#Radios6').exists()).toBeDefined();
      expect(wrapper.find('#Radios7').exists()).toBeDefined();
      expect(wrapper.find('#Radios8').exists()).toBeDefined();

    //   expect(wrapper.find('#xor_operator').exists()).toBeDefined();
    //   expect(wrapper.find('#or_operator').exists()).toBeDefined();
    //   expect(wrapper.find('#and_operator').exists()).toBeDefined();
    //   expect(wrapper.find('#commit-btn').exists()).toBeDefined();
      
  })
});