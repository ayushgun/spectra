import React from 'react';
import {
  ImageBackground,
  StyleSheet,
  View,
} from 'react-native';
import { Text } from 'react-native-paper';
import { useEffect, useRef, useState } from 'react';
import { shareAsync } from 'expo-sharing';
import * as MediaLibrary from 'expo-media-library';
import { StatusBar } from 'expo-status-bar';
import { FAB } from 'react-native-paper';
import { theme } from './core/theme';
import { Camera, NoCameraDeviceError, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';

const Video2 = () => {
  const { hasPermission, requestPermission } = useCameraPermission()

  if (hasPermission === false) {
    return (
      <View style={{ flex: 1, backgroundColor: 'black' }}>
        <Text style={{ color: 'white' }}>No access to camera</Text>
        <Button title="Request Access" onPress={requestPermission} />
      </View>
    )
  }

  const device = useCameraDevice('back')

  if (device == null) return <NoCameraDeviceError />
  return (
    <Camera
      style={styles.container}
      device={device}
      isActive={true}
    >
      <FAB
        icon="menu"
        style={styles.fab}
        onPress={() => navigation.navigate('Settings')}
      />
      <Text>Future implementation of Toast.</Text>
      <StatusBar style="auto" />
    </Camera>
  )

  return (
    <div>Camera</div>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  fab: {
    alignSelf: 'flex-start',
    left: 20,
    top: 0,
    marginBottom: 650,
    opacity: 1,
  },
});

export default Video2