import React from 'react';
import 'react-native-gesture-handler';
import {NavigationContainer} from '@react-navigation/native';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  Button,
  StatusBar,
} from 'react-native';

import {
  Header,
  LearnMoreLinks,
  Colors,
  DebugInstructions,
  ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';
import {createStackNavigator} from '@react-navigation/stack';
import {LoginScreen, ChatScreen, RoomsScreen} from './src/screens';

const Stack = createStackNavigator();

class App extends React.Component {
  render() {
    return (
      <SafeAreaView>
        <NavigationContainer>
          <Stack.Navigator>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Rooms" component={RoomsScreen} />

            <Stack.Screen name="Chat" component={ChatScreen} />
          </Stack.Navigator>
        </NavigationContainer>
      </SafeAreaView>
    );
  }
}

export default App;
